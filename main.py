from ansoegning import PyUdvikler


def main():
    pyudv = PyUdvikler()
    print(
        f"{pyudv.kaldenavn} har søgt jobbet som py-udvikler.\n"
        f"Dette er en gennemgang af {pyudv.stedord.ejefald} ansøgning.\n"
        f"Nu gennemgår vi de {len(pyudv.cases)} cases:"
    )

    for n in range(len(pyudv.cases)):
        res = pyudv.cases[n].beregn()
        print(
            f"case nummer {n+1} er beregnet for {pyudv.kaldenavn}.\n"
            f"{pyudv.stedord.grundform.title()} får resultatet:"
        )
        print(res)


if __name__ == "__main__":
    main()