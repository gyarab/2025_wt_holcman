import httpx
from colorama import Fore, Style, init

CNB_URL = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt"

init(autoreset=True)


def separator():
    print(Fore.BLUE + "=" * 35)


def read_rates():
    try:
        res = httpx.get(CNB_URL, timeout=10.0)
    except Exception as e:
        print(Fore.RED + "Chyba: nelze se připojit k ČNB.")
        print(Fore.YELLOW + f"Detail: {e}")
        return None, None

    if res.status_code != 200:
        print(Fore.RED + f"Nepodařilo se stáhnout kurzovní lístek. HTTP: {res.status_code}")
        return None, None

    lines = res.text.split("\n")
    date = lines[0].split("#")[0].strip()

    rates = {}

    for line in lines[2:]:
        if not line.strip():
            continue
        parts = line.split("|")
        if len(parts) != 5:
            continue

        _, _, amount_str, code, rate_str = parts

        try:
            amount = int(amount_str)
            rate = float(rate_str.replace(",", "."))
        except ValueError:
            continue

        rates[code] = rate / amount

    return date, rates


def read_float(prompt):
    while True:
        raw = input(Fore.CYAN + prompt).strip().replace(",", ".")
        try:
            num = float(raw)
            if num <= 0:
                print(Fore.RED + "Zadej kladné číslo větší než 0.")
                continue
            return num
        except ValueError:
            print(Fore.RED + "Tohle není číslo.")


def read_currency_code(rates):
    while True:
        code = input(Fore.CYAN + "Zadej kód měny (např. EUR, USD, GBP): ").strip().upper()
        if code in rates:
            return code
        print(Fore.RED + "Neznámý kód měny.")
        print(Fore.YELLOW + "Tip: napiš 'L' pro vypsání dostupných kódů.")


def list_currencies(rates):
    codes = sorted(rates.keys())
    separator()
    print(Fore.MAGENTA + Style.BRIGHT + "Dostupné měny z ČNB:")
    for i in range(0, len(codes), 10):
        print(Fore.YELLOW + "  " + " ".join(codes[i:i + 10]))
    separator()


def main():
    print(Fore.MAGENTA + Style.BRIGHT + "\n ČNB převodník měn \n")

    date, rates = read_rates()
    if rates is None:
        return

    while True:
        separator()
        print(Fore.YELLOW + f"Datum kurzu: {date}")
        separator()

        print(Style.BRIGHT + "1) Měna → CZK")
        print("2) CZK → Měna")
        print("3) Znovu načíst kurzy")
        print("L) Vypsat dostupné měny")
        print("Q) Konec\n" + Style.RESET_ALL)

        choice = input(Fore.CYAN + "Vyber: ").strip().upper()

        if choice == "Q":
            print(Fore.GREEN + "Koncim. Cus")
            break

        if choice == "3":
            print(Fore.YELLOW + "Načítám nové kurzy...")
            new_date, new_rates = read_rates()
            if new_rates is not None:
                date, rates = new_date, new_rates
                print(Fore.GREEN + "Hotovo. Kurzy aktualizovány.")
            continue

        if choice == "L":
            list_currencies(rates)
            continue

        if choice == "1":
            separator()
            print(Fore.MAGENTA + "Převod: Měna → CZK")
            print(Fore.YELLOW + "Pro vypsání měn napiš v dalším kroku místo kódu: L")
            code = input(Fore.CYAN + "Zadej kód měny: ").strip().upper()
            if code == "L":
                list_currencies(rates)
                code = read_currency_code(rates)
            elif code not in rates:
                print(Fore.RED + "Neznámý kód měny.")
                continue

            amount = read_float(f"Zadej částku v {code}: ")
            czk = amount * rates[code]

            print(Fore.GREEN + Style.BRIGHT + f"\n {amount:.2f} {code} = {czk:.2f} CZK")
            print(Fore.WHITE + f"(Kurz: 1 {code} = {rates[code]:.4f} CZK)")
            separator()
            print()
            continue

        if choice == "2":
            separator()
            print(Fore.MAGENTA + "Převod: CZK -> Měna")
            print(Fore.YELLOW + "Pro vypsání měn napiš v dalším kroku místo kódu: L")
            code = input(Fore.CYAN + "Zadej kód měny: ").strip().upper()
            if code == "L":
                list_currencies(rates)
                code = read_currency_code(rates)
            elif code not in rates:
                print(Fore.RED + "Neznámý kód měny.")
                continue

            czk = read_float("Zadej částku v CZK: ")
            amount = czk / rates[code]

            print(Fore.GREEN + Style.BRIGHT + f"\n {czk:.2f} CZK = {amount:.2f} {code}")
            print(Fore.WHITE + f"(Kurz: 1 {code} = {rates[code]:.4f} CZK)")
            separator()
            print()
            continue

        print(Fore.RED + "Neplatná volba. Zkus 1, 2, 3, L nebo Q.\n")


if __name__ == "__main__":
    main()
