import matplotlib.pyplot as plt
import csv
import os

# ── Read FASTA ──────────────────────────────────────────────
def read_fasta(file_path):
    sequences = {}
    current_name = ""
    current_seq = ""
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith(">"):
                if current_name:
                    sequences[current_name] = current_seq
                current_name = line.strip()[1:]
                current_seq = ""
            else:
                current_seq += line.strip()
        if current_name:
            sequences[current_name] = current_seq
    return sequences

# ── Analysis Functions ───────────────────────────────────────
def nucleotide_count(seq):
    return {"A": seq.count("A"), "T": seq.count("T"),
            "G": seq.count("G"), "C": seq.count("C")}

def gc_content(seq):
    g = seq.count("G")
    c = seq.count("C")
    return ((g + c) / len(seq)) * 100

def at_gc_ratio(seq):
    at = seq.count("A") + seq.count("T")
    gc = seq.count("G") + seq.count("C")
    return round(at / gc, 2) if gc != 0 else 0

def reverse_complement(seq):
    complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
    return "".join(complement[base] for base in reversed(seq))

# ── Plot ─────────────────────────────────────────────────────
def plot_nucleotides(counts, seq_name):
    bases = list(counts.keys())
    values = list(counts.values())
    colors = ["#4CAF50", "#2196F3", "#FF5722", "#FFC107"]
    plt.figure(figsize=(6, 4))
    plt.bar(bases, values, color=colors)
    plt.title(f"Nucleotide Composition - {seq_name}")
    plt.xlabel("Nucleotide")
    plt.ylabel("Count")
    plt.tight_layout()
    os.makedirs("../results", exist_ok=True)
    plt.savefig(f"../results/{seq_name}_plot.png")
    plt.close()
    print(f"Plot saved for {seq_name}")

# ── Save CSV ─────────────────────────────────────────────────
def save_csv(all_results):
    with open("../results/summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Sequence", "Length", "A", "T", "G", "C",
                         "GC%", "AT/GC Ratio"])
        for r in all_results:
            writer.writerow([r["name"], r["length"],
                             r["counts"]["A"], r["counts"]["T"],
                             r["counts"]["G"], r["counts"]["C"],
                             r["gc"], r["at_gc"]])
    print("CSV saved to results/summary.csv")

# ── Main ─────────────────────────────────────────────────────
def main():
    file_path = "../data/sample.fasta"
    sequences = read_fasta(file_path)
    all_results = []

    for name, sequence in sequences.items():
        print(f"\n--- {name} ---")
        counts = nucleotide_count(sequence)
        gc = gc_content(sequence)
        ratio = at_gc_ratio(sequence)
        rev_comp = reverse_complement(sequence)

        print(f"Length         : {len(sequence)}")
        print(f"Nucleotides    : {counts}")
        print(f"GC Content     : {gc:.2f}%")
        print(f"AT/GC Ratio    : {ratio}")
        print(f"Rev Complement : {rev_comp[:50]}...")

        plot_nucleotides(counts, name)
        all_results.append({
            "name": name, "length": len(sequence),
            "counts": counts, "gc": round(gc, 2), "at_gc": ratio
        })

    save_csv(all_results)
    with open("../results/output.txt", "w") as f:
        for r in all_results:
            f.write(f"\n--- {r['name']} ---\n")
            f.write(f"Length: {r['length']}\n")
            f.write(f"Counts: {r['counts']}\n")
            f.write(f"GC Content: {r['gc']}%\n")
            f.write(f"AT/GC Ratio: {r['at_gc']}\n")

if _name_ == "_main_":
    main()
