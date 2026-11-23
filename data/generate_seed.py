"""Write the synthetic seed data of the two test companies (Story 1.6; FR-3, AD-8, AD-15).

    uv run python data/generate_seed.py

writes data/seed/testbedrift-a.json and testbedrift-b.json. The output is the
same on every run and on every platform: the series use integer arithmetic and
noise from SHA-256 of the product number and the position, and nothing reads a
clock or a random generator. The rule test products and Strøsand 25 kg take
their series and stock from reference/reference-examples.xlsx, the answer key
(AD-17), so the product screen and the spreadsheet show the same case.
data/README.md documents the schema and the products.
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from django.contrib.auth.hashers import PBKDF2PasswordHasher

DATA_DIR = Path(__file__).resolve().parent
REFERENCE_DIR = DATA_DIR.parent / "reference"
SCHEMA_VERSION = 1
# The noise of a week, in percent of its level, is −NOISE…+NOISE.
NOISE = 20


def flat(level):
    return ("flat", level)


def trend(start, step_hundredths):
    return ("trend", start, step_hundredths)


def seasonal(base, amplitude):
    return ("seasonal", base, amplitude)


def made(number, name, stock, shape, weeks=104, tail=None, patches=None):
    """A product made by the generator: a shape, then edits in the workbook's
    notation: `tail` for the last weeks, and `patches` by the number of weeks
    before the last one, so {6: "21"} sets the sixth week from the end."""
    return {
        "number": number,
        "name": name,
        "stock": stock,
        "shape": shape,
        "weeks": weeks,
        "tail": tail,
        "patches": patches or {},
    }


def written(number, name, stock, series):
    """A product with a series written out in the workbook's notation."""
    return {"number": number, "name": name, "stock": stock, "series": series}


def stable(number, name, level):
    """A stable product with 104 weeks and stock that covers three weeks."""
    return made(number, name, level * 3, flat(level))


# Each company: its login, a fixed salt of at least 22 letters and digits (the
# length at which Django's must_update accepts a salt, so a login does not
# rewrite the hash), the products made here, and the products that come from the
# workbook by the workbook's name: (product number, name).
COMPANIES = [
    {
        "file": "testbedrift-a.json",
        "company": "A",
        "customer_number": "1001",
        "name": "Testbedrift A",
        "password": "testbedrift-a",
        "salt": "prognoseSeedTestbedriftA",
        "latest_week": (2026, 45),
        "from_workbook": {
            "Strøsand 25 kg": ("10012", "Strøsand 25 kg"),
            "E8": ("10025", "Impregnert planke 48×98 mm, 3 m"),
        },
        "products": [
            # The products of «Denne uken» (UX-DR46): the last three weeks give
            # the week-1 forecast of the mockup, 8,0 for Isskrape and so on.
            made("10007", "Isskrape", 2, flat(8), tail="7, 9, 8"),
            made("10031", "Lyspære LED E27 9 W", 12, flat(19), tail="19, 18, 19"),
            made(
                "10004",
                "Skruer 4×40 mm, 200 stk.",
                20,
                flat(8),
                tail="22, 21, 21",
                patches={6: "21", 5: "22", 4: "21", 3: "22"},
            ),
            written("10040", "Snøskuffe aluminium", 6, "4, 6"),
            made("10001", "Malertape 25 mm", 40, flat(9), tail="9, 9, 10"),
            made("10002", "Kabelstrips 200 mm", 25, flat(7), tail="6, 7, 7"),
            made("10019", "Tetningslist 6 m", 14, flat(3), weeks=80, tail="3, 3, 3"),
            stable("10020", "Hammer 500 g", 12),
            stable("10021", "Skrutrekkersett, 6 deler", 30),
            stable("10022", "Tommestokk 5 m", 9),
            stable("10023", "Arbeidshansker str. 9", 25),
            stable("10024", "Sandpapir korn 120", 40),
            stable("10026", "Maling hvit 2,7 l", 14),
            stable("10027", "Pensel 50 mm", 18),
            stable("10028", "Trelim 250 ml", 10),
            stable("10029", "Silikon transparent", 16),
            stable("10030", "Batteri AA, 4 pk.", 22),
            stable("10032", "Ledning 3×1,5 mm², per meter", 35),
            stable("10033", "Skjøteledning 10 m", 60),
            stable("10034", "Stikkontakt utenpåliggende", 20),
            stable("10035", "Spiker 50 mm, 1 kg", 45),
            stable("10036", "Treskrue 5×60 mm, 200 stk.", 50),
            stable("10037", "Plugg 8 mm, 100 stk.", 28),
            stable("10038", "Vinkelbeslag 40 mm", 15),
            stable("10039", "Hengsel 75 mm", 11),
            stable("10041", "Dørhåndtak børstet stål", 24),
            stable("10042", "Hengelås 40 mm", 32),
            stable("10043", "Gaffateip 50 m", 13),
        ],
    },
    {
        "file": "testbedrift-b.json",
        "company": "B",
        "customer_number": "1002",
        "name": "Testbedrift B",
        "password": "testbedrift-b",
        "salt": "prognoseSeedTestbedriftB",
        "latest_week": (2026, 44),
        "from_workbook": {
            "E1": ("20001", "Plantejord 20 l"),
            "E7": ("20002", "Plengjødsel 10 kg"),
            "E9": ("20003", "Hageslange 25 m"),
            "E10": ("20004", "Frøpose gulrot"),
            "E15": ("20005", "Terrakottapotte 30 cm"),
            "E16": ("20006", "Vannkanne 10 l"),
            "E18 a": ("20007", "Sagblad 250 mm"),
            "E18 b": ("20008", "Hagesaks"),
            "E19": ("20009", "Kompostbeholder"),
        },
        "products": [
            made("20010", "Grillkull 10 kg", 30, seasonal(20, 50)),
            made("20011", "Hagekalk 20 kg", 20, trend(10, 20)),
            made(
                "20012",
                "Tørrfôr hund 15 kg",
                30,
                flat(14),
                patches={40: "S", 39: "S", 9: "S", 8: "S"},
            ),
            made(
                "20013",
                "Blomsterjord 40 l",
                40,
                flat(12),
                patches={6: "40", 2: "40"},
            ),
            made(
                "20014",
                "Gjerdestolpe 1,8 m",
                30,
                flat(8),
                tail="22, 21, 21",
                patches={6: "21", 5: "22", 4: "21", 3: "22"},
            ),
            made(
                "20015",
                "Parasoll 2 m",
                0,
                flat(10),
                patches={n: "S" for n in range(10)},
            ),
            made("20016", "Stearinlys, 10 pk.", 100, flat(10)),
            made("20017", "Slangekobling messing", 5, flat(15)),
            written("20018", "Solcellelykt", 12, "S, 4, S, 6, S"),
            made("20019", "Kattemat 2 kg", 20, flat(14), weeks=12),
            made("20020", "Fuglefrø 5 kg", 20, flat(14), weeks=11),
            made("20021", "Hagestol, sammenleggbar", 15, flat(12), weeks=60),
            stable("20022", "Plantegjødsel flytende 1 l", 12),
            stable("20023", "Såjord 10 l", 20),
            stable("20024", "Rive stål", 9),
            stable("20025", "Spade", 10),
            stable("20026", "Gressfrø 1 kg", 18),
            stable("20027", "Ugressduk 10 m", 11),
            stable("20028", "Plastsekk 120 l, 10 pk.", 25),
            stable("20029", "Lyslenke utendørs", 16),
            stable("20030", "Fuglehus tre", 9),
            stable("20031", "Plantestøtte bambus", 30),
            stable("20032", "Vanningskobling", 22),
        ],
    },
]


def noise(product_number, position):
    digest = hashlib.sha256(f"{product_number}:{position}".encode()).digest()
    return int.from_bytes(digest[:4], "big") % (2 * NOISE + 1) - NOISE


def level_hundredths(shape, position, week_number):
    """The level of a week in hundredths of a unit, from integers only."""
    if shape[0] == "flat":
        return shape[1] * 100
    if shape[0] == "trend":
        return shape[1] * 100 + shape[2] * (position - 1)
    # A triangular season: the peak at week 26 is +amplitude percent, and the
    # trough at week 52 or 1 is −amplitude percent.
    _, base, amplitude = shape
    distance = abs((week_number - 1) % 52 - 26)
    return base * (100 + amplitude * (26 - 2 * distance) // 26)


def monday_of(year, week):
    return date.fromisocalendar(year, week, 1)


def parse_week(text):
    year, week = re.fullmatch(r"(\d{4})-W(\d{2})", text).groups()
    return int(year), int(week)


def week_label(monday):
    iso = monday.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def series_of(spec, latest_monday, parse_sales):
    """Return a product's weeks as a list of (units sold, stockout) pairs."""
    if "series" in spec:
        return [(w.units_sold, w.stockout) for w in parse_sales(spec["series"])]
    count = spec["weeks"]
    first = latest_monday - timedelta(weeks=count - 1)
    weeks = []
    for position in range(1, count + 1):
        week_number = (first + timedelta(weeks=position - 1)).isocalendar().week
        level = level_hundredths(spec["shape"], position, week_number)
        units = (level * (100 + noise(spec["number"], position)) + 5000) // 10000
        weeks.append((units, False))
    if spec["tail"]:
        tail = parse_sales(spec["tail"])
        if len(tail) > count:
            raise ValueError(
                f"product {spec['number']}: the tail is longer than the history"
            )
        weeks[count - len(tail) :] = [(w.units_sold, w.stockout) for w in tail]
    for from_end, token in spec["patches"].items():
        if not 0 <= from_end < count:
            raise ValueError(
                f"product {spec['number']}: no week {from_end} from the end"
            )
        week = parse_sales(token)[0]
        weeks[count - 1 - from_end] = (week.units_sold, week.stockout)
    return weeks


def product_record(number, name, stock, weeks, latest_monday):
    return {
        "product_number": number,
        "name": name,
        "first_week": week_label(latest_monday - timedelta(weeks=len(weeks) - 1)),
        "units_sold": [units for units, _ in weeks],
        "stockout_positions": [
            position for position, (_, out) in enumerate(weeks, 1) if out
        ],
        "stock_on_hand": stock,
    }


def build_companies(workbook=None):
    """Return the companies of the seed files, as the files hold them."""
    # The reader sits in reference/, which is on the path under pytest but not
    # when this file runs as a script.
    if str(REFERENCE_DIR) not in sys.path:
        sys.path.insert(0, str(REFERENCE_DIR))
    import answer_key_reader

    rows = {}
    for row in answer_key_reader.read_typed(
        "products", workbook or answer_key_reader.WORKBOOK
    ):
        key = row.get("product")
        missing = [c for c in ("company", "sales", "stock_on_hand") if c not in row]
        if key in rows or missing:
            raise ValueError(
                f"the workbook's product {key!r} is listed twice"
                if key in rows
                else f"the workbook's product {key!r} lacks {', '.join(missing)}"
            )
        rows[key] = row
    placed = {key for c in COMPANIES for key in c["from_workbook"]}
    if set(rows) != placed:
        raise ValueError(
            f"the workbook's products {sorted(set(rows) - placed)} are placed in no "
            f"company, and {sorted(placed - set(rows))} are not in the workbook"
        )
    hasher = PBKDF2PasswordHasher()
    companies = []
    for company in COMPANIES:
        latest_monday = monday_of(*company["latest_week"])
        products = []
        for key, (number, name) in company["from_workbook"].items():
            row = rows[key]
            if row["company"] != company["company"]:
                raise ValueError(
                    f"the workbook places {key!r} in company {row['company']}, "
                    f"not {company['company']}"
                )
            weeks = [(w.units_sold, w.stockout) for w in row["sales"]]
            products.append(
                product_record(number, name, row["stock_on_hand"], weeks, latest_monday)
            )
        for spec in company["products"]:
            weeks = series_of(spec, latest_monday, answer_key_reader.parse_sales)
            products.append(
                product_record(
                    spec["number"], spec["name"], spec["stock"], weeks, latest_monday
                )
            )
        products.sort(key=lambda product: product["product_number"])
        companies.append(
            {
                "file": company["file"],
                "latest_week": week_label(latest_monday),
                "data": {
                    "schema_version": SCHEMA_VERSION,
                    "customer_number": company["customer_number"],
                    "name": company["name"],
                    "password_hash": hasher.encode(
                        company["password"], company["salt"]
                    ),
                    "products": products,
                },
            }
        )
    validate(companies)
    return companies


def end_week(product):
    """The ISO week of a product's last position."""
    year, week = parse_week(product["first_week"])
    last = monday_of(year, week) + timedelta(weeks=len(product["units_sold"]) - 1)
    return week_label(last)


def validate(companies):
    """Raise ValueError for seed data that breaks AD-8 or FR-3's shape."""
    numbers = set()
    customers = set()
    for company in companies:
        data = company["data"]
        products = data["products"]
        if not 10 <= len(products) <= 50:
            raise ValueError(f"{data['name']} has {len(products)} products, not 10–50")
        if not data["customer_number"].isdigit():
            raise ValueError(f"{data['name']}: a bad customer number")
        if data["customer_number"] in customers:
            raise ValueError(f"customer number {data['customer_number']} is used twice")
        customers.add(data["customer_number"])
        if len({p["name"] for p in products}) != len(products) or not all(
            p["name"] for p in products
        ):
            raise ValueError(f"{data['name']}: a product name is empty or used twice")
        if any(not p["units_sold"] for p in products):
            raise ValueError(f"{data['name']}: a product has no weeks")
        ends = {end_week(product) for product in products}
        if ends != {company["latest_week"]}:
            raise ValueError(
                f"{data['name']}: the products end at {sorted(ends)}, "
                f"not at {company['latest_week']}"
            )
        for product in products:
            number = product["product_number"]
            if not re.fullmatch(r"\d{5}", number):
                raise ValueError(f"product number {number!r} is not 5 digits")
            if number in numbers:
                raise ValueError(f"product number {number} is used twice")
            numbers.add(number)
            length = len(product["units_sold"])
            positions = product["stockout_positions"]
            if length < 1 or positions != sorted(set(positions)):
                raise ValueError(f"product {number}: a bad series")
            if positions and not 1 <= positions[0] <= positions[-1] <= length:
                raise ValueError(f"product {number}: a stockout week out of range")
            if any(units < 0 for units in product["units_sold"]):
                raise ValueError(f"product {number}: negative sales")
            if product["stock_on_hand"] < 0:
                raise ValueError(f"product {number}: negative stock on hand")


def dumps(data):
    """JSON with a fixed layout: two spaces, each list of numbers on one line."""
    text = json.dumps(data, indent=2, ensure_ascii=False)

    def one_line(match):
        return "[" + ", ".join(re.findall(r"-?\d+", match[0])) + "]"

    return re.sub(r"\[\s+-?\d[-\d,\s]*\]", one_line, text) + "\n"


def write(companies, output_dir):
    # Render every file before the first is opened, so a failure leaves no
    # half-written pair.
    texts = {company["file"]: dumps(company["data"]) for company in companies}
    output_dir.mkdir(parents=True, exist_ok=True)
    for company in companies:
        path = output_dir / company["file"]
        with path.open("w", encoding="utf-8", newline="\n") as file:
            file.write(texts[company["file"]])
        print(f"Skrev {path.name}: {len(company['data']['products'])} produkter.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--output-dir", type=Path, default=DATA_DIR / "seed")
    parser.add_argument("--workbook", type=Path, default=None)
    arguments = parser.parse_args(argv)
    try:
        companies = build_companies(arguments.workbook)
    except ValueError as error:
        raise SystemExit(f"Seed-filene ble ikke skrevet: {error}") from error
    write(companies, arguments.output_dir)


if __name__ == "__main__":
    main()
