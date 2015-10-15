

from xml.dom import minidom
import sys
import os


def extract_species(filename):  # reading from SBMl file to extract species
    myFile = open(filename, "r")
    xmldoc = minidom.parse(myFile)
    
    spiclist = xmldoc.getElementsByTagName('species')
    
    namelist = []
    idlist = []
    for s in spiclist :
        dict_species ={}
        namelist.append(s.attributes['name'].value)
        idlist.append(s.attributes['id'].value)
        
    dict_species = dict(zip(idlist,namelist))
    return(dict_species)


def write_species(dict_species,filename): # create xml file based on list of species in order to seprate complex species 
    
    doc = minidom.Document()
    root = doc.createElement('CompositionOfSpecies')
    doc.appendChild(root)


    # Create Element
    keys = sorted(dict_species.keys())
    for key in keys:
        tempChild = doc.createElement('species')
        tempChild.setAttribute("id",key)
        tempChild.setAttribute("name",dict_species[key])
        root.appendChild(tempChild)
        if dict_species[key].find(":")!= -1:
            s = dict_species[key].split(':')
            for c in s:
                subelm = doc.createElement('atomic')
                tempChild.appendChild(subelm)    
                subelm.setAttribute("count",'1')
                subelm.setAttribute("name",c)
        else:
            subelm = doc.createElement('atomic')
            tempChild.appendChild(subelm)
            subelm.setAttribute("count",'1')
            subelm.setAttribute("name",dict_species[key])
    
   # write in xmlfile
    doc.writexml( open(filename, 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
    
    doc.unlink()

def write_atomic_refinement(in_file,out_file): # create refinment.xml file to store refined atomics 
    File = open(in_file, "r")
    xmldoc = minidom.parse(File)
    doc = minidom.Document()
    root = doc.createElement('AtomicRefinement')
    doc.appendChild(root)
    re = []
    refine = set(xmldoc.getElementsByTagName('atomic'))
    for r in refine:
        if r.attributes['name'].value not in re:
           re.append(r.attributes['name'].value)
    
    for j in range (0,len(re)):   
       
        atomChild = doc.createElement('atomic')
        atomChild.setAttribute("name",re[j])
        root.appendChild(atomChild)
        rechild = doc.createElement('refined')
        rechild.setAttribute("name",'r'+ re[j])
        atomChild.appendChild(rechild)
    
#write in xmlfile
    doc.writexml( open(out_file, 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
    
    doc.unlink()
    
def read_species(file): # read the species.xml file in order to create dictionary of that 
    
    dict_species_with_atomic = {}
    dic ={}
    File = open(file, "r")
    xmldoc = minidom.parse(File)

    for i in range (0,len(xmldoc.getElementsByTagName('species'))):
        atomic_count = []
        atomic_name = [] 
        species_id = []
        atomlist = xmldoc.getElementsByTagName('species')[i].getElementsByTagName('atomic')
        species_element = xmldoc.getElementsByTagName('species')
        for s in atomlist :
            atomic_count.append(s.attributes['count'].value)
            atomic_name.append(s.attributes['name'].value)
   
        for n in species_element:
            species_id.append(n.attributes['id'].value)
        dict_species_with_atomic[species_id[i]]= list(zip(atomic_name,atomic_count)) # create dictionary (assign every species to count and name of atomic)
    return dict_species_with_atomic

     
def  read_atomic_refinement(f): # read the atomic_refinement.xml file in order to create dictionary of that 
  
    dict_atomic_refinement = {}
    Fil = open(f, "r")
    xmldoc = minidom.parse(Fil)
    for i in range (0,len(xmldoc.getElementsByTagName('atomic'))):
        refined_list=[]
        atomic_list=[]
    
        refined_element= xmldoc.getElementsByTagName('atomic')[i].getElementsByTagName('refined')
        atomic_element = xmldoc.getElementsByTagName('atomic')
        for r in refined_element:
            refined_list.append(r.attributes['name'].value)
              
        for a in atomic_element:
            atomic_list.append(a.attributes['name'].value)
        
        dict_atomic_refinement[atomic_list[i]] = refined_list  # create dictionary (assign every atomic to the refined atomic
    
    return(dict_atomic_refinement)

def generate_complex_refinement(file,f): # create dictionary (assign every

    d1 = read_species(file) #read the species.xml file in order to create dictionary of that 
    d2 =  read_atomic_refinement(f) # read the atomic_refinement.xml file in order to create dictionary of that 
    dict_complex_refinement_generated = {}
    for key in d1:
        res = [[]]
        for i in range(0,len(d1[key])):
            count = int(d1[key][i][1]) # count  1
            item = (d1[key][i][0])     # atomic  hsf
            leng = len(d2[item])       # number of refined atomic  = 3 = {hsfa,hsfb,hsfc}
            
            
            for m in range (0,count):
                new =[]
                for n in range (0,leng):
                    for j in range(0,len(res)):
                       new.append(sorted(res[j]+[d2[item][n]])) # 
                res=new
          
            new_elem = []
            for elem in res:
                if elem not in new_elem:  # remove duplicate ...
                    new_elem.append(elem)
            res = new_elem
            #print(res)
        dictup = {}
        tup = ()
        for n in range(0,len(res)):
            d = {}
            atmitm =''
            lis = list (set(res[n])) # remove duplicate refined atomic [rhsfa,rhsfa] ---> lis = rhsfa 
            for l in range(0,len(lis)):
                itm= lis[l]  # here rhsfa
                cont=res[n].count(itm)# cont =2
                d[itm]= cont  # {rhsfa:2}
                if cont > 1:
                    atmitm = atmitm + ":" +str(itm) + "_" + str(cont) # :rhsfa_2
                else:
                    atmitm = atmitm + ":" + str(itm)   
            a = d.keys()
            b = d.values()
            tup=list(zip(a,b)) # (rhsfa,2),..
            dictup[atmitm[1:]] = tup # {rhsfa_2:(rhsfa,2)}
        dict_complex_refinement_generated[key]= dictup # {hsf:{rhsfa_2:(rhsfa,2)}}
        
    return(dict_complex_refinement_generated)       #  create dictionary based on complex refinement


def write_complex_refinement(dict_complex_refinement_generated,filename): # create XML file (complex_refinement.xml)
    
    doc = minidom.Document()
    root = doc.createElement('ComplexRefinement')

    doc.appendChild(root)
    
    # Create Element
    keys = sorted(dict_complex_refinement_generated.keys())
    
    for key in keys:
        
        tempChild = doc.createElement('species')
        tempChild.setAttribute("id",key)
        root.appendChild(tempChild)
        m =list( dict_complex_refinement_generated[key].keys())
        
        for n in m:
            elm = doc.createElement('refined')
            tempChild.appendChild(elm)
            elm.setAttribute("name",n)
            
            lis = dict_complex_refinement_generated[key][n]
            
            for r in lis:
                subelm = doc.createElement('atomic')
                elm.appendChild(subelm)
                subelm.setAttribute("count",str(r[1]))
                subelm.setAttribute("name",r[0])
    

  #write in xmlfile
    doc.writexml( open(filename, 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
    
    doc.unlink()                  
            
def read_complex_refinement(filename):# ( it is the same)
    dict_complex_refinement_read ={}
    
    myFile = open(filename, "r")
    xmldoc = minidom.parse(myFile)
    for i in range (0,len(xmldoc.getElementsByTagName('species'))):
      
       species_list = []
       refined_atomic_list = []
       
       refined_dic={}
       
       refined_element = xmldoc.getElementsByTagName('species')[i].getElementsByTagName('refined')
       
       
       species_element = xmldoc.getElementsByTagName('species')

       for m in  species_element:
           species_list.append(m.attributes['id'].value)
           
       for r in refined_element:
          refined_atomic_list.append(r.attributes['name'].value)
       
       for j in range (0,len(refined_atomic_list)):
           atomic_count = []
           atomic_name = []
           atomic_element = xmldoc.getElementsByTagName('species')[i].getElementsByTagName('refined')[j].getElementsByTagName('atomic')    
           for a in atomic_element:
               atomic_count.append(a.attributes['count'].value)
               atomic_name.append(a.attributes['name'].value)
           
           refined_dic[refined_atomic_list[j]]= list(zip(atomic_name,atomic_count))    
       dict_complex_refinement_read[species_list[i]]=refined_dic
    return ( dict_complex_refinement_read)

def read_reactions(filename):
    reaction =[]
    #dict_species= extract_species(filename) # retrieving species dictionary
    
    myFile = open(filename,"r")
    xmldoc = minidom.parse(myFile)
    for i in range (0,len(xmldoc.getElementsByTagName('reaction'))):
       reactant_species = []
       reactant_stoichiometry = []
       product_species = []
       product_stoichiometry = []
    
       if xmldoc.getElementsByTagName('reaction')[i].getElementsByTagName('listOfReactants')!= []:
           reactant = xmldoc.getElementsByTagName('reaction')[i].getElementsByTagName('listOfReactants')[0].getElementsByTagName('speciesReference')
       else:
           reactant = []
       if xmldoc.getElementsByTagName('reaction')[i].getElementsByTagName('listOfProducts') != []:
           product = xmldoc.getElementsByTagName('reaction')[i].getElementsByTagName('listOfProducts')[0].getElementsByTagName('speciesReference')
       else:
           product= []   

       for r in reactant:
           reactant_species.append(r.attributes['species'].value)
           reactant_stoichiometry.append(r.attributes['stoichiometry'].value)
     
       
       for p in product:
            
            product_species.append(p.attributes['species'].value)
           
            product_stoichiometry.append(p.attributes['stoichiometry'].value)
          

       reaction.append((list(zip(reactant_species,reactant_stoichiometry)),list(zip(product_species,product_stoichiometry)))) 
    #print("\n reaction",reaction)
    return (reaction)      

def generate_reactions(reactions,dict_complex_refinement_read):
   
    left_side = {}
    right_side = {}
    
    for i in range (0, len(reactions)):
                    
                    left_side[i] = reactions[i][0]
                    right_side[i]= reactions[i][1]

    d1 = left_side
    d2 =  dict_complex_refinement_read
    dict_left = {}
    for key in d1:
        res = [[]]
        for i in range(0,len(d1[key])):
            count = int(d1[key][i][1])
            #print("count",count)
            item = (d1[key][i][0])
            #print("item",item)
            leng = len(d2[item])
            #print("leng",leng)
            for m in range (0,count):
                new =[]
                for n in range (0,leng):
                    for j in range(0,len(res)):
                       new.append(sorted(res[j]+[list (d2[item].keys())[n]])) # 
                res=new
            new_elem = []
            for elem in res:
                if elem not in new_elem:  # remove duplicate ...
                    new_elem.append(elem)
            res = new_elem
            #print("res",res)
            #print("********************************************")
        dictup = {}
        tup = ()
        for n in range(0,len(res)):
            d = {}
            atmitm =''
            lis = list (set(res[n]))
            for l in range(0,len(lis)):
                itm= lis[l]
                cont=res[n].count(itm)
                d[itm]= cont
                if cont > 1:
                    atmitm = atmitm + ":" +str(itm) + "_" + str(cont)
                else:
                    atmitm = atmitm + ":" + str(itm)   
            a = d.keys()
            b = d.values()
            tup=list(zip(a,b))
            dictup[atmitm[1:]] = tup
        dict_left[key]= dictup
        #print("dict_left[key]",dict_left[key])
    d1 = right_side
    d2 =  dict_complex_refinement_read
    dict_right = {}
    for key in d1:
        res = [[]]
        for i in range(0,len(d1[key])):
            count = int(d1[key][i][1])
            item = (d1[key][i][0])
            leng = len(d2[item])
            for m in range (0,count):
                new =[]
                for n in range (0,leng):
                    for j in range(0,len(res)):
                       new.append(sorted(res[j]+[list (d2[item].keys())[n]])) # 
                res=new
            new_elem = []
            for elem in res:
                if elem not in new_elem:  # remove duplicate ...
                    new_elem.append(elem)
            res = new_elem
        dictup = {}
        tup = ()
        for n in range(0,len(res)):
            d = {}
            atmitm =''
            lis = list (set(res[n]))
            for l in range(0,len(lis)):
                itm= lis[l]
                cont=res[n].count(itm)
                d[itm]= cont
                if cont > 1:
                    atmitm = atmitm + ":" +str(itm) + "_" + str(cont)
                else:
                    atmitm = atmitm + ":" + str(itm)   
            a = d.keys()
            b = d.values()
            tup=list(zip(a,b))
            dictup[atmitm[1:]] = tup
        dict_right[key]= dictup
    reaction_dic = {}
    for d in dict_left:
        
        result =[]
        left_list =(list (dict_left[d].values()))
        
        right_list =( list (dict_right[d].values()))
        
        for i in range(0,len(left_list)):
            for j in range (0,len(right_list)):
                tup = (left_list[i], right_list[j])
                
                result.append(tup)
                reaction_dic[d]= result
       
    return (reaction_dic)

def  write_reaction(dict_species_with_atomic,dict_atomic_refinement,dict_complex_refinement_read,reaction_dic,filename):
    
    doc = minidom.Document()
    root =doc.createElement('sbml')
    doc.appendChild(root)
    root.setAttribute('xmlns',"http://www.sbml.org/sbml/level3/version1/core" )
    root.setAttribute('level',"3")
    root.setAttribute('version',"1")
    
    modelChild = doc.createElement('model')
    root.appendChild(modelChild)
    modelChild.setAttribute('id','Refined_Model')

    list_compart = doc.createElement('listOfCompartments')
    modelChild.appendChild(list_compart)
    comChild =  doc.createElement('compartment')
    list_compart.appendChild(comChild)
    comChild.setAttribute('id','cell')
    comChild.setAttribute('name','cell')
    comChild.setAttribute("constant",'false')

   
    
    list_species = doc.createElement('listOfSpecies')
    modelChild.appendChild(list_species)
    
   
    all_species = list(reaction_dic.values())
    
    lis = []
    for k in  all_species:
        for l in range (0,len(k)):
            for m in range (0,len(k[l])):
                for n in range (0,len(k[l][m])):
                    lis.append(k[l][m][n][0])
    lis = list(set(lis))
    for li in lis:
        specChild = doc.createElement('species')
        list_species.appendChild(specChild)
        
        if li.find(":")== -1:
           specChild.setAttribute('id',li)
        if (li.find(":")!= -1) and (li.find(" ")!= -1):
            new=li.replace(":",'_').replace(" ","_")
            specChild.setAttribute('id',new)
            
            
        if li.find(" ")!= -1:
             new=li.replace(" ","_")
             specChild.setAttribute('id',new)
        if li.find(":")!= -1:
            new=li.replace(":",'_')
            specChild.setAttribute('id',new)
            
       
           
            
       
        specChild.setAttribute('name',li)
        specChild.setAttribute('compartment','cell')
        specChild.setAttribute("constant",'false')
        specChild.setAttribute("hasOnlySubstanceUnits",'true')
        specChild.setAttribute("boundaryCondition",'false')
    
    list_reaction = doc.createElement('listOfReactions')
    modelChild.appendChild(list_reaction)

    
    
   
    # Create Element
    keys = sorted(reaction_dic.keys())
    j = 0
    for key in keys:
        
        for i in range (0,len(reaction_dic[key])):
            tempChild = doc.createElement('reaction')
            tempChild.setAttribute('id','r' + str(j))
            j = j+1
            tempChild.setAttribute('reversible','false')
            tempChild.setAttribute('fast','false')
            list_reaction.appendChild(tempChild)
            left = reaction_dic[key][i][0]
            right = reaction_dic[key][i][1]
            if left != []:
                elm = doc.createElement('listOfReactants')
                tempChild.appendChild(elm)
            if right != []:
                elme = doc.createElement('listOfProducts')
                tempChild.appendChild(elme)
            
               
            for l in left:
                subelm = doc.createElement('speciesReference')
                elm.appendChild(subelm)
                subelm.setAttribute("stoichiometry",str(l[1]))
                if l[0].find(":")== -1:
                    subelm.setAttribute("species",l[0])
                if (l[0].find(":")!= -1) and (l[0].find(" ")!= -1) :
                    new=l[0].replace(":",'_').replace(" ","_")
                    subelm.setAttribute("species",new)
                if l[0].find(" ")!= -1:
                    new=l[0].replace(" ","_")
                    subelm.setAttribute("species",new)
                if l[0].find(":")!= -1:
                    new=l[0].replace(":",'_')
                    subelm.setAttribute("species",new)
                subelm.setAttribute("constant",'false')
            for r in right:
                sub = doc.createElement('speciesReference')
                elme.appendChild(sub)
                sub.setAttribute("stoichiometry",str(r[1]))
                if r[0].find(":")== -1:
                    sub.setAttribute("species",r[0])
                if (r[0].find(":")!= -1) and (r[0].find(" ")!= -1) :
                    new=r[0].replace(":",'_').replace(" ","_")
                    sub.setAttribute("species",new)
                if r[0].find(" ")!= -1:
                    new=r[0].replace(" ","_")
                    sub.setAttribute("species",new)
                if r[0].find(":")!= -1:
                    new=r[0].replace(":",'_')
                    sub.setAttribute("species",new)
                
                sub.setAttribute("constant",'false')
                
                
    annotChild1 = doc.createElement('annotation')
    modelChild.appendChild(annotChild1)
    inside_annot= doc.createElement('AdditionalInformation')
    annotChild1.appendChild(inside_annot)

    
    List_Species = doc.createElement('CompositionOfSpecies')

    inside_annot.appendChild(List_Species)

    # Create Element
    key1 = sorted(dict_species_with_atomic.keys())
   

    for key in key1:
        tempChild = doc.createElement('species')
        tempChild.setAttribute("id",key)
        tempChild.setAttribute("name",key)
        List_Species.appendChild(tempChild)
        m = list(dict_species_with_atomic[key])
        
        for i in range(0, len(m)):
            elm = doc.createElement('atomic')
            tempChild.appendChild(elm)
            elm.setAttribute("name",m[i][0])
            elm.setAttribute("count",str(m[i][1]))
            
    refin = doc.createElement('AtomicRefinement')
    inside_annot.appendChild(refin)
    
    key2 = sorted(dict_atomic_refinement.keys())
    
    for key in key2:
        tempChild = doc.createElement('atomic')
        tempChild.setAttribute("name",key)
        List_Species.appendChild(tempChild)
        m = list(dict_atomic_refinement[key])
        for i in range(0, len(m)):
            elm = doc.createElement('refined')
            tempChild.appendChild(elm)
            elm.setAttribute("name",m[i])
            
    
        
    
    complex_refin = doc.createElement('ComplexRefinement')
    inside_annot.appendChild(complex_refin)
    
    # Create Element
    key3 = sorted(dict_complex_refinement_read.keys())
    
    for key in key3:
        
        tempChild = doc.createElement('Species')
        tempChild.setAttribute("id",key)
        complex_refin.appendChild(tempChild)
        m =list( dict_complex_refinement_read[key].keys())
        
        for n in m:
            elm = doc.createElement('refined')
            tempChild.appendChild(elm)
            elm.setAttribute("name",n)
            lis = dict_complex_refinement_read[key][n]
            for r in lis:
                subelm = doc.createElement('atomic')
                elm.appendChild(subelm)
                subelm.setAttribute("count",str(r[1]))
                subelm.setAttribute("name",r[0])
      
  #write in xmlfile
    doc.writexml( open(filename, 'w'),
                  indent="  ",addindent="  ",encoding = "UTF-8",
                  newl='\n')
    
    doc.unlink()

def print_chemical_reaction(filename): # orginal model or refined model file "  printing all reaction with substrate and products
    reaction =[]
    dict_species= extract_species(filename) # retrieving species dictionary
    
    myFile = open(filename,"r")
    xmldoc = minidom.parse(myFile)
    for i in range (0,len(xmldoc.getElementsByTagName('reaction'))):
       reactant_species = []
       reactant_stoichiometry = []
       product_species = []
       product_stoichiometry = []
    
       if xmldoc.getElementsByTagName('reaction')[i].getElementsByTagName('listOfReactants')!= []:
           reactant = xmldoc.getElementsByTagName('reaction')[i].getElementsByTagName('listOfReactants')[0].getElementsByTagName('speciesReference')
       else:
           reactant = []
       if xmldoc.getElementsByTagName('reaction')[i].getElementsByTagName('listOfProducts') != []:
           product = xmldoc.getElementsByTagName('reaction')[i].getElementsByTagName('listOfProducts')[0].getElementsByTagName('speciesReference')
       else:
           product= []   

       for r in reactant:
           reactant_species.append(dict_species[r.attributes['species'].value])
           reactant_stoichiometry.append(r.attributes['stoichiometry'].value)
     
       
       for p in product:
            
            product_species.append(dict_species[p.attributes['species'].value])
           
            product_stoichiometry.append(p.attributes['stoichiometry'].value)
          

       reaction.append((list(zip(reactant_species,reactant_stoichiometry)),list(zip(product_species,product_stoichiometry)))) 

    s2= []
    for i in range(len(reaction)):
        s1 = ""
        j=0
        while (j< len(reaction [i])):
            
            z = 0
            if j == 1:
                s1 = s1+ ' --> '
                
            while True:
                if z < (len(reaction [i][j]))-1:
                    if (int(reaction[i][j][z][1]))> 1:
                        s1= s1+(str(reaction[i][j][z][1]+ reaction[i][j][z][0])) + ' + '
                        
                    else:
                        s1= s1+(str(reaction[i][j][z][0])) + ' + '
                        
                        
                elif z == (len(reaction [i][j]))-1:
                    if (int(reaction[i][j][z][1]))> 1:
                        s1= s1 +( str(reaction[i][j][z][1]+ reaction[i][j][z][0]))       
                    else:
                        s1 = s1 + (str(reaction[i][j][z][0]))
                    break
                elif (len(reaction [i][j])) == 0:
                    break
                z = z+1
                
            j = j+1
            
        s2.append(s1)
    return(s2)
        







