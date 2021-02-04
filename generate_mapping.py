import numpy as np
import sys 

def print_table_in_latex():
    # function used to print the mapping table in latex form.
    def str_msg_label(msg_name):
        if '-' not in msg_name:
            return msg_name
        else:
            msg_name = msg_name.split('-')
            num = msg_name[1][0]
            return msg_num[0] + '\\bar{' + msg_name[1][0] + '}' + msg_name[1][1:]
    
    def str_Cms(Cms):
        if len(Cms) == 0:
            return ' '
        else:
            assert len(Cms) in [1,2,3]
            Cms_str = []
            for Cm in Cms:
                if all([ -10 < ii < 10 for ii in Cm]):
                    Cm_str = ''.join( [ str(mm) if mm>=0 else '\\overline{'+str(abs(mm))+'}' for mm in Cm ] )
                else:
                    Cm_str = ','.join( [ str(mm) if mm>=0 else '\\overline{'+str(abs(mm))+'}' for mm in Cm ] )
                Cms_str.append('$' + Cm_str +'$')
            return ' & '.join( xx for xx in Cms_str )
    
    def str_inva(inv):
        inv = str(inv) if inv > 0 else '\\overline{' + str(abs(inva)) + '}'
        return '$' + inv + '$'
    
    def str_ind(ind, ind_group = None):
        return ''.join([ str(i) for i in ind ]) if ind_group != None and all([ ii < 10 for ii in ind_group ]) \
                else ','.join([ str(i) for i in ind ])

    mapping_data = np.load("MSG_mapping_data.npy",allow_pickle=True)

    save_file = open('mapping_table.tex','w')
    save_file.write('\\documentclass[9pt]{article}\n'+\
                    '\\usepackage[utf8]{inputenc}\n'+\
                    '\\usepackage[margin=1in]{geometry}\n'+\
                    '\\geometry{a4paper,scale=0.6}\n'+\
                    '\\usepackage{graphicx,float}\n'+\
                    '\\usepackage{multirow}\n'+\
                    '\\usepackage{makecell}\n'+\
                    '\\usepackage{amsmath,amssymb}\n'+\
                    '\\usepackage{longtable}\n'+\
                    '\\usepackage{dcolumn}\n'+\
                    '\\title{Mapping table of symmetry-based indicators and topological invariants in magnetic space groups}\n'+\
                    '\\begin{document}\n'+\
                    '\\maketitle\n'+\
                    '\\begin{longtable}{c|c|' + 'c'*18 + '}\n')
    for msg_data in mapping_data:
        bns_num, bns_label, msg_type, classification = msg_data['bns_num'], msg_data['bns_label'], msg_data['msg_type'], msg_data['classification']
        SI_group, SI_set, SI_name = msg_data['X_BS'], msg_data['ind_values'], msg_data['Ind_name']
        inv_set, inv_type, inv_name = msg_data['invariants_values'], msg_data['invariants_type'], msg_data['invariants_name']

        point_ops_name_new, mirror_ops_name = inv_name[-2], inv_name[-1]
        mag_trans = inv_name[1][0] + ' & ' if msg_type == 4 else '' 

        # print the first row of each msg_num
        save_file.write('\\hline\n')
        save_file.write('\\multicolumn{20}{c}{' + bns_num + '\ \ \ ' + '$' + str_msg_label(bns_label) + '$' + \
                        '\ \ \  Classification = $' + classification + '$ \ \ \ ' +\
                        '$\\text{X}_{\\text{BS}}=\\mathbb{Z}_{' + str_ind(SI_group) + '}$\ \ \ SI = ' + SI_name + '}\n')
        save_file.write('\\\\\hline\n')
 
        # print the second row of ops names:
        save_file.write(' $\\mathbb{Z}_{' + str_ind(SI_group) + '}$  & weak & ' + mag_trans + \
                        ' & '.join([name for name in point_ops_name_new]) + ' & ' + \
                        ' & '.join([name for name in mirror_ops_name]) + '\n')       
        save_file.write('\\\\\hline\n')

        # print each SI:
        for ind_, inv_ in zip(SI_set, inv_set):
            if msg_type in [1,3] :
                save_file.write('$' + str_ind(ind_, SI_group) + '$ & ' + \
                            '(' + ''.join(str_inva(w) for w in inv_[0]) + ')' + ' & ' \
                                + ' & '.join([str_inva(xx) for xx in inv_[1]]) \
                                + ' & ' + str_Cms(inv_[2]) + '\n')
            else:
                save_file.write('$' + str_ind(ind_, SI_group) + '$' + ' & ' + \
                            '(' + ''.join(str_inva(w) for w in inv_[0]) + ')' \
                                + ' & ' + str_inva(inv_[1][0]) + ' & ' \
                                + ' & '.join([str_inva(xx) for xx in inv_[2]]) \
                                + ' & ' + str_Cms(inv_[3]) + '\n')

            save_file.write('\\\\\hline\n')

        save_file.write('\\hline\n')

    save_file.write('\\end{longtable}\n')
    save_file.write('\\end{document}\n')
    save_file.close()



def load_data(msg_num, input_SI = None):
    # Function used to print the required mapping data for an MSG
    # For a given MSG and an SI set, find the corresponding invariant sets
    def print_data(ind, inv):
        print('%20s    %s'%(str(ind), str(inv)))

    def add_inv(l1, l2, inv_type):
        output = []
        assert len(l2) in [3,4], l2
        if len(l2) == 3:
            output.append([ i1 + i2 for i1, i2 in zip(l1[0], l2[0]) ]) # weak
            output.append([ i1 + i2 if mod != 2 else (i1 + i2) % mod for i1, i2, mod in zip(l1[1], l2[1], inv_type) ]) # other inv 
            output.append([[i1 + i2 for i1, i2 in zip(m1, m2) ] for m1, m2 in zip(l1[2], l2[2])]) if len(l1[2]) > 0 else output.append([]) # mirror
        else:
            output.append([ i1 + i2 for i1, i2 in zip(l1[0], l2[0]) ]) # weak
            output.append((l1[1] + l2[1]) % 2)
            output.append([ i1 + i2 if mod != 2 else (i1 + i2) % mod for i1, i2, mod in zip(l1[1], l2[1], inv_type) ]) # other inv 
           #output.append([ i1 + i2 for i1, i2 in zip(l1[2], l2[2]) ]) # other inv
            output.append([[i1 + i2 for i1, i2 in zip(m1, m2) ] for m1, m2 in zip(l1[3], l2[3])]) if len(l1[2]) > 0 else output.append([]) # mirror
        return output

    mapping_data = np.load("MSG_mapping_data.npy",allow_pickle=True)
    locate_msg = [ tmp['bns_num'] == msg_num for tmp in mapping_data ]
    assert sum(locate_msg) == 1, ('Input MSG number not exist! Please input BNS number of the MSG.')
    msg_data = mapping_data[locate_msg.index(1)]
    
    ind_set, ind_group = msg_data['ind_values'], msg_data['X_BS']
    inv_set, inv_name, inv_type = msg_data['invariants_values'], msg_data['invariants_name'], msg_data['invariants_type']
    
    if input_SI != None: 
        assert len(input_SI) == len(ind_group), ('Input SI wrong! SI group=',str(ind_group))

    print('MSG:', msg_num, '  X_BS:', ind_group)
    print('%20s    %s'%('Indicator', str(inv_name)))
    if input_SI != None:    
        # 1. print SI=0
        null_inv = []
        for ind, inv in zip(ind_set, inv_set):
            if sum(ind) == 0:
                print_data(ind, inv)
                null_inv.append(inv)

        print()
        # 2. print input SI 
        for ind, inv in zip(ind_set, inv_set):
            if np.sum(np.abs(np.array(ind) - np.array(input_SI))) == 0:
                for null_ in null_inv:
                    inv_new = add_inv(inv, null_, inv_type)
                    print_data(ind, inv_new)
                break
    else:
        for ind, inv in zip(ind_set, inv_set):
            print_data(ind, inv)
 

if __name__ == '__main__': 

    if len(sys.argv) <=1:
        print('Please give the magnetic space group number and an indicator set, e.g,\
                    \npython generate_mapping.py 2.4 \'[1,1,1,2]\'')
    elif len(sys.argv) == 2:
        msg_num = sys.argv[1]
        input_SI = None
    elif len(sys.argv) == 3:
        msg_num = sys.argv[1]
        input_SI = [ int(i) for i in sys.argv[2].strip('[]').split(',') ]
    else:
        print('Please give the magnetic space group number and an indicator set, e.g.,\
                    \npython generate_mapping.py 2.4 \'[1,1,1,2]\'')
        
    load_data(msg_num, input_SI)

