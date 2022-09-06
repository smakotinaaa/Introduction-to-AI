import sys


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    domain_file.write("Propositions:\n")
    for disk in disks:
        for peg in pegs:
            domain_file.write(f"{disk}_on_{peg} ")
        domain_file.write(f"{disk}_top_ ")
    for first_disk_ind, first_disk in enumerate(disks):
        for second_disk_ind, second_dsk in enumerate(disks[first_disk_ind+1:]):
            domain_file.write(f"{first_disk}_on_{second_dsk} ")
    for peg in pegs:
        domain_file.write(f"E{peg} ")
    domain_file.write("Actions:\n")
    # Move from a disk to a disk
    for move_disk_ind, disk_to_move in enumerate(disks):
        for load_disk in disks[move_disk_ind+1:]:
            for unload_disk in disks[move_disk_ind+1:]:
                if load_disk != unload_disk:
                    domain_file.write(f"Name: move_{disk_to_move}_from_{load_disk}_to_{unload_disk}\n")
                    domain_file.write(f"pre: {disk_to_move}_top_ {disk_to_move}_on_{load_disk} {unload_disk}_top_\n")
                    domain_file.write(f"add: {load_disk}_top_ {disk_to_move}_on_{unload_disk}\n")
                    domain_file.write(f"delete: {disk_to_move}_on_{load_disk} {unload_disk}_top_\n")
    # Move from a disk to a peg
    for move_disk_ind, disk_to_move in enumerate(disks):
        for load_disk in disks[move_disk_ind+1:]:
            for unload_peg in pegs:
                domain_file.write(f"Name: move_{disk_to_move}_from_{load_disk}_to_{unload_peg}\n")
                domain_file.write(f"pre: {disk_to_move}_top_ {disk_to_move}_on_{load_disk} E{unload_peg}\n")
                domain_file.write(f"add: {load_disk}_top_ {disk_to_move}_on_{unload_peg}\n")
                domain_file.write(f"delete: {disk_to_move}_on_{load_disk} E{unload_peg}\n")
    # Move from a peg to a disk
    for move_disk_ind, disk_to_move in enumerate(disks):
        for load_peg in pegs:
            for unload_disk in disks[move_disk_ind+1:]:
                domain_file.write(f"Name: move_{disk_to_move}_from_{load_peg}_to_{unload_disk}\n")
                domain_file.write(f"pre: {disk_to_move}_top_ {disk_to_move}_on_{load_peg} {unload_disk}_top_\n")
                domain_file.write(f"add: E{load_peg} {disk_to_move}_on_{unload_disk}\n")
                domain_file.write(f"delete: {disk_to_move}_on_{load_peg} {unload_disk}_top_\n")
    # Move from a peg to a peg
    for move_disk_ind, disk_to_move in enumerate(disks):
        for load_peg in pegs:
            for unload_peg in pegs:
                if load_peg != unload_peg:
                    domain_file.write(f"Name: move_{disk_to_move}_from_{load_peg}_to_{unload_peg}\n")
                    domain_file.write(f"pre: {disk_to_move}_top_ {disk_to_move}_on_{load_peg} E{unload_peg}\n")
                    domain_file.write(f"add: E{load_peg} {disk_to_move}_on_{unload_peg}\n")
                    domain_file.write(f"delete: {disk_to_move}_on_{load_peg} E{unload_peg}\n")
    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    problem_file.write("Initial state: ")
    problem_file.write(f"{disks[0]}_top_ ")
    for i in range(len(disks) - 1):
        problem_file.write(f"{disks[i]}_on_{disks[i+1]} ")
    problem_file.write(f"{disks[-1]}_on_{pegs[0]} ")
    for peg in pegs[1:]:
        problem_file.write(f"E{peg} ")
    problem_file.write(f"\n")
    problem_file.write("Goal state: ")
    problem_file.write(f"{disks[0]}_top_ ")
    for i in range(len(disks) - 1):
        problem_file.write(f"{disks[i]}_on_{disks[i+1]} ")
    problem_file.write(f"{disks[-1]}_on_{pegs[-1]} ")
    for peg in pegs[:-1]:
        problem_file.write(f"E{peg} ")
    problem_file.write(f"\n")
    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
