# DNA Sequence Analyzer

def read_fasta(file_path):
    sequence = ""
    with open(file_path, "r") as file:
        for line in file:
            if not line.startswith(">"):
                sequence += line.strip()
    return sequence


def nucleotide_count(seq):
    return {
        "A": seq.count("A"),
        "T": seq.count("T"),
        "G": seq.count("G"),
        "C": seq.count("C")
    }


def gc_content(seq):
    g = seq.count("G")
    c = seq.count("C")
    return ((g + c) / len(seq)) * 100


def main():
    file_path = "../data/sample.fasta"

    sequence = read_fasta(file_path)

    counts = nucleotide_count(sequence)
    gc = gc_content(sequence)

    print("Sequence Length:", len(sequence))
    print("Nucleotide Counts:", counts)
    print("GC Content: {:.2f}%".format(gc))

    # Save results
    with open("../results/output.txt", "w") as f:
        f.write(f"Length: {len(sequence)}\n")
        f.write(f"Counts: {counts}\n")
        f.write(f"GC Content: {gc:.2f}%\n")


if _name_ == "_main_":
    main()