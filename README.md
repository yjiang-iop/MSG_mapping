# *MSG_mapping*
This tool contains the quantitative mapping table between symmetry-based indicators (SIs) and topological invariants in 1421 magnetic space groups (MSGs). It also contains the irreducible co-representation (co-irrep) matrices of 1651 Shubnikov space groups (SSGs).

More details can be found in the following work:
- [*Topological classification and diagnosis in magnetically ordered electronic materials*](https://arxiv.org/abs/2102.12645), Bingrui Peng, Yi Jiang, Zhong Fang, Hongming Weng, Chen Fang.


## Mapping tables
- `mapping_table.pdf` is the collection of all mapping tables in 1421 MSGs.

    For each MSG, we first list the bases of the null space of the mappings, and all the other invariant sets with zero indicators can be generated by combining these bases. Then for each nonzero indicator set, we list one possible invariant set. Other possible invariant sets can be generated by adding invariant sets with zero indicators.
   
   The latex file of this table can be generated using the `print_table_in_latex(）` function in `generate_mapping.py`

- The python file `generate_mapping.py` can be used to generate the invariant sets that corresponding to a specific input indicator set of an MSG:
    ```python
    python generate_mapping.py msg_num ind_set
    ```
   where `msg_num` is a string denoting the BNS number of a MSG, e.g., `'2.4'`, and `ind_set` is a list of indicator, e.g., `'[1,1,1,2]'`.
   
## Co-irrep data
- We give the co-irrep data of 1651 SSGs in the `data` folder, where the data of each SSG is listed in a file named by its BNS number. For each high-symmetry point (HSP), we first tabulate its little group generators, and for each co-irrep, the representation matrices of generators.
