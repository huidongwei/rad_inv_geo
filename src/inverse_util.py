##
import os
import glob

def read_FEA_disp(res_sty_file):

    file_name = res_sty_file + ".sty"

    with open(file_name,"r") as line:

        data = line.readlines()

    disp_label = False

    disp_array = []

    for data_line in data:

        if "Displacement" in data_line:
            #print("displacement data found")
            disp_label = True

        if disp_label:
            try:
                disp = []

                disp_node_label = int(data_line[0:8])

                disp.append(disp_node_label)

                disp_node_x = float(data_line[8:24])
                disp.append(disp_node_x)

                disp_node_y = float(data_line[24:40])
                disp.append(disp_node_y)

                disp_node_z = float(data_line[40:56])
                disp.append(disp_node_z)

                #print(disp_node_label, disp_node_x, disp_node_y, disp_node_z)
                disp_array.append(disp)

            except ValueError:
                print("not displacement data")

    return disp_array

##
def update_msh_coord(old_msh_file, disp_array, new_msh_file):

    disp_num = len(disp_array)       
    nod_ind = [disp_array[i][0] for i in range(disp_num)]
    # print(nod_ind)

    file_temp = open(old_msh_file + ".inc","r")
    file_update = open("cylinder_new_relabel_exec.inc","w")
    file_write = open(new_msh_file + ".inc","w")

    node_label = False
    shell_label = False

    line_num = 0
    for line in file_temp:

        line_num = line_num + 1
        new_line = line

        if "/NODE" in line and not "/GRNOD" in line:
            #print("node definition found")
            node_label = True
            shell_label = False
        
        elif "/BRICK" in line and not("/GRBRIC" in line): 
            #print("shell definition found")
            node_label = False
            shell_label = True
        
        if node_label:
            #new_line = line
            data = new_line.split()
            #print(data)
            
            if data[0].isnumeric():
            
                node = int(data[0])
                node_X = float(data[1])
                node_Y = float(data[2])
                node_Z = float(data[3])   
                            
                ind = nod_ind.index(node)

                new_line = "{0:10d}".format(node)+"{0:20.5e}".format(node_X + disp_array[ind][1])+\
                    "{0:20.5e}".format(node_Y + disp_array[ind][2])+"{0:20.5e}".format(node_Z + disp_array[ind][3])+'\n'
                
        file_update.write(new_line)
        file_write.write(new_line)

    file_temp.close()
    file_update.close() 
    file_write.close()

    return 0

def update_msh_coord_relax(old_msh_file, disp_array, ref_msh_pos, new_msh_file, relax = 1.0):

    disp_num = len(disp_array)       
    nod_ind = [disp_array[i][0] for i in range(disp_num)]
    # print(nod_ind)

    disp_num = len(ref_msh_pos)       
    nod_ind_ref = [ref_msh_pos[i][0] for i in range(disp_num)]    
    

    file_temp = open(old_msh_file + ".inc","r")
    file_update = open("cylinder_new_relabel_exec.inc","w")
    file_write = open(new_msh_file + ".inc","w")

    node_label = False
    shell_label = False

    line_num = 0
    for line in file_temp:

        line_num = line_num + 1
        new_line = line

        if "/NODE" in line and not "/GRNOD" in line:
            #print("node definition found")
            node_label = True
            shell_label = False
        
        elif "/BRICK" in line and not("/GRBRIC" in line): 
            #print("shell definition found")
            node_label = False
            shell_label = True
        
        if node_label:
            #new_line = line
            data = new_line.split()
            #print(data)
            
            if data[0].isnumeric():
            
                node = int(data[0])
                node_X = float(data[1])
                node_Y = float(data[2])
                node_Z = float(data[3])   
                            
                ind = nod_ind.index(node)
                ind_ref = nod_ind_ref.index(node)

                new_line = "{0:10d}".format(node)
                
                update = node_X*(1.0 - relax)+ relax*(ref_msh_pos[ind_ref][1]-disp_array[ind][1])
                new_line = new_line + "{0:20.5e}".format(update)
                
                update = node_Y*(1.0 - relax)+ relax*(ref_msh_pos[ind_ref][2]-disp_array[ind][2])
                new_line = new_line + "{0:20.5e}".format(update)
                
                update = node_Z*(1.0 - relax)+ relax*(ref_msh_pos[ind_ref][3]-disp_array[ind][3])
                new_line = new_line + "{0:20.5e}".format(update)
                
                new_line = new_line + '\n'
                
        file_update.write(new_line)
        file_write.write(new_line)

    file_temp.close()
    file_update.close() 
    file_write.close()

    return 0
##
def get_msh_pos(msh_file):

    file_temp = open(msh_file + ".inc","r")
    node_label = False
    shell_label = False

    line_num = 0
    node_pos = []

    for line in file_temp:

        line_num = line_num + 1
        new_line = line

        if "/NODE" in line and not "/GRNOD" in line:
            #print("node definition found")
            node_label = True
            shell_label = False
        
        elif "/BRICK" in line and not("/GRBRIC" in line): 
            #print("shell definition found")
            node_label = False
            shell_label = True

        elif "/GRNOD" in line: 
            #print("shell definition found")
            node_label = False
            shell_label = False
            
        if node_label:
            #new_line = line
            data = new_line.split()
            #print(data)
            
            if data[0].isnumeric():
                
                nod_temp = []
                node = int(data[0])
                nod_temp.append(node)

                node_X = float(data[1])
                nod_temp.append(node_X)

                node_Y = float(data[2])
                nod_temp.append(node_Y)

                node_Z = float(data[3])  
                nod_temp.append(node_Z) 
                            
                node_pos.append(nod_temp)

    file_temp.close()

    return node_pos

##
def tol_cal(ref_msh_pos,update_msh_pos):

    res_tol = 0

    disp_num = len(update_msh_pos) 

    nod_ind = [update_msh_pos[i][0] for i in range(disp_num)]

    diff_array = []

    for i in range(len(ref_msh_pos)):

        diff_temp = []
        
        diff_temp.append(ref_msh_pos[i][0])

        node_ind_loc = nod_ind.index(ref_msh_pos[i][0])

        for j in range(1,4):

            diff = ref_msh_pos[i][j]-update_msh_pos[node_ind_loc][j]

            res_tol = res_tol + diff**2

            diff_temp.append(diff)

        diff_array.append(diff_temp)

    return res_tol, diff_array

##
def run_radioss_bat():


    command = "run_mpi_cyd.bat"

    os.system(command)

    return 0
    
def del_radioss_rst():

    cwd = os.getcwd()
    
    for item in os.listdir(cwd):
        
        if item.endswith(".rst") or item.endswith(".tmp"):
        
            os.remove(os.path.join(cwd, item))
            
    pattern = r"*DESKTOP*"
    
    for item in glob.iglob(pattern, recursive=True):
        
        os.remove(item)