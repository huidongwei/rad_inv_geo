from inverse_util import *
import shutil

def opt_operation(start = 0, max_loop = 1000, relax = 0.5):

    max_loop = max_loop

    tol_set = 1E-3

    msh_file = "cylinder_new_relabel"

    ref_msh_pos = get_msh_pos(msh_file)
    
    res_tol = 1000
    
    
    if start==0:
    
        shutil.copy("cylinder_new_relabel_0.inc", "cylinder_new_relabel_exec.inc")
        rec_file = open("optimisation.dat","w")
        
        line = "#process_num, " + "#tolerance" + '\n'        
        rec_file.write(line)
        
    else:
        rec_file = open("optimisation.dat","a")

    for i in range(start,max_loop):

        old_msh_file = "cylinder_new_relabel_" + str(i)
        new_msh_file = "cylinder_new_relabel_" + str(i+1)
        
        #Run the radioss to acquire the displacement
        #and update the old mesh file to new mesh file
        del_radioss_rst()
        run_radioss_bat() 
        disp_array = read_FEA_disp("pressure_LAW42_0002")
        update_msh_coord(old_msh_file, disp_array, new_msh_file)   
        
        #get the updated mesh coordinates
        update_msh_pos = get_msh_pos(new_msh_file)
        
        #compare the new mesh file with reference to get the difference
        res_tol, msh_diff_array = tol_cal(ref_msh_pos,update_msh_pos)
        #use difference to correct the old mesh file to new mesh file
        
        #update_msh_coord(old_msh_file, msh_diff_array, new_msh_file)
        
        update_msh_coord_relax(old_msh_file, disp_array, ref_msh_pos, new_msh_file, relax = relax)
        
        #line = "process_num:{0:5d},".format(i) + "tolerance:{0:20.5e}".format(res_tol)+'\n'
        line = "{0:5d},".format(i) + "{0:20.5e}".format(res_tol)+'\n'
        
        rec_file.write(line)

        print("tolerance of current file {0:5d} is: ".format(i), res_tol)
        
        del_radioss_rst()

        if res_tol < tol_set:

            break
            
    rec_file.close()

opt_operation(start = 0, max_loop = 40, relax = 0.8)
