import os
import env as path
import datetime as dt
from handle_json import *
from config_handle import *
from configparser import ConfigParser

def prompt_clients(list_clients_b=True):
    """
    Displays a numbered list of clients and allows the user to select one.

    Args:
        list_clients_b (bool, optional): Determines whether the list of clients should be obtained from a specific directory
            (default) or if a list of clients is provided directly. Defaults to True.

    Returns:
        dict: A dictionary mapping the selected index numbers to the names of the clients.

    Example Usage:
        # Displays a list of clients obtained from the default directory and allows the user to select one
        prompt_clients()

        # Displays a list of clients provided directly and allows the user to select one
        clients_list = ['client1', 'client2', 'client3']
        prompt_clients(list_clients_b=False)
    """
    list_clients = os.listdir(path.PATTERN_PATH) if list_clients_b == True else list_clients_b 
    if list_clients == []:
        return create_folder()
    clients_dict ={list_clients.index(i) + 1 : i for i in list_clients} 
    clients_texted = '      \n+---+------------------------------------------------\n'.join(['| ' 
                                                            + str(list(clients_dict.keys())[i]) 
                                                            + ' | ' 
                                                            + clients_dict[list(clients_dict.keys())[i]] for i in range(len(clients_dict))])
    print(f"""
Selecione um cliente pelo número, na lista abaixo
+---+------------------------------------------------
{clients_texted}
+---+------------------------------------------------
    """)    
    return clients_dict

def create_folder():
    """
    Creates a new folder for a client.

    Prompts the user to input the name of the client to be created.
    Creates a new folder with the client's name within the specified directory.
    Prints a message confirming the addition of the new client.
    Returns to the main program menu.
    """
    name = input('Digite o nome do cliente que deseja criar: ')
    try:
        path_clients = os.path.join(path.PATTERN_PATH, name)
        os.mkdir(path_clients)
        print("\nNovo cliente Adicionado! Retornando ao menu principal.")
    except Exception as e:
        print(f"\nFalha ao criar a pasta pelo motivo abaixo:\n{e}\nEm caso de dúvida, procure a equipe de TI")

def rename_alias(verify=True):
    """
    Renames or creates aliases for client folders.

    Reads the client aliases from the "client_alias.json" file.
    Lists all clients within the specified directory.
    If verify is True, prompts the user to enter an alias for each client folder not already assigned an alias.
    If verify is False, prompts the user to select a client to rename their alias.
    Updates the client alias dictionary and saves it to the "client_alias.json" file.
    Returns to the main program menu after creating or updating an alias.
    """
    alias = read_file("client_alias.json")
    list_clients = os.listdir(path.PATTERN_PATH)
    if verify == True:
        for i in list_clients:
            if alias.get(i) == None:
                i_alias = input(f"digite abaixo qual apelido para as pastas você deseja dar para o cliente : {i}\n")
                update_file({i: i_alias}, "client_alias.json")
    else:
        clients_dict = prompt_clients()
        while True:
            selected_client = input("Selecione o número correspondente do cliente que gostaria de mudar o apelido: ")
            if clients_dict.get(int(selected_client)) != None:
                print(f"\nVocê selecionou o cliente : {clients_dict.get(int(selected_client))}")
                break
        set_alias = input(f"digite abaixo qual apelido para as pastas desse cliente você deseja endereçar?\n")
        while True:
            confirmation = input(f"""Você escolheu o apelido '{set_alias}' para o cliente '{clients_dict.get(int(selected_client))}'
tem certeza da sua escolha? Digite 'S' para Sim, e 'N' para Não >>> """)
            if confirmation.upper() == 'S':
                break
            elif confirmation.upper() == 'N':
                print("Apelido não alterado! Retornando ao menu principal")
                return 0
        app_obj = {clients_dict.get(int(selected_client)) : set_alias}
        update_file(app_obj, 'client_alias.json')
        print('Apelido criado/alterado! Retornando ao menu principal.')
        
def get_client_alias(client):
    """
    Gets the client's alias from a JSON file of aliases.

    Args:
        client (str): The name of the client for which the alias is desired.

    Returns:
        str or None: The client's alias if it exists in the JSON file of aliases. 
                     Returns None if there is no alias for the client.

    Raises:
        FileNotFoundError: If the JSON file of aliases cannot be found.
    """
    alias_file = read_file('client_alias.json')
    alias = alias_file.get(client)
    if alias != None:
        return alias
    else:
        rename_alias(False)

def create_multiple_sub(inner_folder: list, outer_folder: str):
    """
    Creates folders within a given outer folder.

    Parameters:
    - inner_folder (list): List containing names of the folders to be created within the outer folder.
    - outer_folder (str): Path of the outer folder where the inner folders will be created.

    Returns:
    No explicit return.
    """
    for i in inner_folder:
        inner_folder = os.path.join(outer_folder, i)
        os.makedirs(inner_folder)


def create_subfolders(folder_name: str):
    """
    Creates a standard folder structure.

    Parameters:
    - folder_name (str): Name of the project.

    Returns:
    No explicit return.
    """
    arr_obj = folder_name.split('_')
    os.mkdir('00_Doc')
    os.mkdir('01_Referencia')
    os.mkdir('02_Projeto')
    create_multiple_sub(['01_Premiere', '02_DavinciResolve', '03_AfterEffects'], '02_Projeto')
    os.mkdir('03_Video')
    create_multiple_sub(['00_Video_Bruto', '01_Stock_Video', '02_VFX'], '03_Video')
    create_multiple_sub([arr_obj[0] + '_Canon01/Proxy', arr_obj[0] + '_Drone01/Proxy', arr_obj[0] + '_Red01/Proxy', arr_obj[0] + "_BM01/Proxy"], '03_Video/00_Video_Bruto/')
    os.mkdir('04_Audio')
    create_multiple_sub(['00_Sonora', '01_Loc', '02_Trilhas', '03_SFX', '04_Mix'], '04_Audio')
    create_multiple_sub([arr_obj[0] + '_Audio01'], '04_Audio/00_Sonora/')
    os.mkdir('05_Imagem')
    os.mkdir('06_GC')
    os.mkdir('07_Color_Render')
    create_multiple_sub(['00_Davinci_IN', '01_Davinci_OUT'], '07_Color_Render')
    os.mkdir('08_Export')
    create_multiple_sub(['00_Video_OffLine', '01_Audio_para_Mix', '03_XML', '04_Legenda'], '08_Export')
    create_multiple_sub(['00_Para_Premiere', '01_Para_Davinci'], '08_Export/03_XML')
    os.mkdir('09_Entrega')

def get_last_job(client_dir):
    list_clients = os.listdir(client_dir)
    print("\nABRINDO PROCESSO DE ESCOLHA DO NÚMERO DO JOB\n")
    if list_clients == []:
        print("A pasta não possui jobs, determine o número do primeiro job")
        while True:
            vl = input("O número do primeiro job será: ")
            try : return int(vl)
            except : print("Não foi possível converter o texto acima em número, tente novamente")
    else:
        jobs = [0]
        for job in list_clients:
            try:
                job_num = int(str(job).split("_")[1].replace("JOB", ""))
                jobs.append(job_num)
            except:
                print(f"warning - pasta: {job} não segue modelo especificado")
                pass
        last_job = max(jobs)
        while True:
            vl = input(f"Último Job >>> {last_job}, aperte ENTER se deseja que o próximo seja : {last_job + 1}, caso não, escreva o número do job >> ")
            if vl == '': 
                vl = last_job + 1
            try : return int(vl)
            except : print("Não foi possível converter o texto acima em número, tente novamente")
    
def set_folder():
    """
    This function assists in creating a directory structure to store files for a 
    specific job of a particular client.

    The user is guided through a series of interactive prompts to select the client,
    input job details, and confirm directory creation.

    Returns:
        None

    Raises:
        ValueError: If the entered date is not valid.

    """
    clients_dict = prompt_clients()
    rename_alias()
    
    while True:
        selected_client = input("Selecione o número correspondente ao cliente desejado: ")
        selected_client_name = clients_dict.get(int(selected_client))
        year = str(dt.datetime.now().year)
        client_dir = path.PATTERN_PATH + '/' + selected_client_name + '/'+ year
        if selected_client_name != None:
            print(f"\nVocê selecionou o cliente : {selected_client_name}")
            break
        else:
            print('Esse número não corresponde a nenhum cliente, tente novamente. ')

    if not os.path.exists(client_dir):
        print(f"A pasta {year} não existe, criando pasta {year}...")
        os.mkdir(client_dir)

    while True:
        try:    
            job_num = get_last_job(client_dir)
            job_name = input("\nInsira o nome do job: ").title().replace(' ' , '')
            if len(job_name) == 0:
                print("Você não deu um nome ao seu job")
            else: break
        except :
            if KeyboardInterrupt:
                print("saindo do Módulo")
                return 0
            else:            
                print("Número de Job Inválido.")
    while True:
        choose_date = input(f"""
o job foi solicitado na data de hoje({dt.datetime.strftime(dt.datetime.now(), "%d/%m/%Y")})?

APERTE 'ENTER' SE SIM | ou digite 'N' e aperte ENTER se NÃO """)
        if choose_date == '':
            date_vl = dt.datetime.strftime(dt.datetime.now(), "%y%m%d")
            break
        elif choose_date.lower() == 'n':
            day_in = input("\nDigite o dia desejado: ")
            month_in = input("\nDigite o mês desejado: ")
            year_in = input("\nDigite o ano desejado: ")
        try: 
            date_vl = dt.datetime(int(year_in), int(month_in), int(day_in)).strftime("%y%m%d")
            break
        except:
            print("A data digitada não é válida, tente novamente")
    client_alias = get_client_alias(selected_client_name)
    zero_repeat = '0' * (4 - len(str(job_num)))
    job_concat = f"{date_vl}_JOB{zero_repeat}{job_num}_{client_alias}_{job_name}"
    dir_validate = input(f"O nome do job é {job_concat}, aperte 'N' se deseja recomeçar: ")
    if dir_validate.lower() == 'n':
        set_folder()
    os.chdir(client_dir)
    os.mkdir(job_concat)
    os.chdir(job_concat)
    create_subfolders(job_concat)



def menu_set():
    """
    Presents a menu of options for performing various actions related to creating client and project folders.

    Prompts the user to choose an option between creating a folder for a project, creating or assigning an alias for a client folder, or creating a new client.
    Directs the user to the corresponding function based on the chosen option.
    If the chosen option is not valid, prompts the user to choose again.
    """
    given_option = int(input("""
    O que gostaria de fazer?
    1. Criar uma pasta para um projeto
    2. Criar um cliente
    3. Crie ou dê um apelido para uma pasta de um cliente                         
    
    selecione o número correspondente: """))
    match given_option:
        case 1:
            set_folder()
        case 2:
            create_folder()
            print("Retornando ao MENU!")
            menu_set()
        case 3:
            rename_alias(False)
            menu_set()
        case _:
            print("Não identifiquei a sua escolha, por favor escolha novamente. ")
            menu_set()

if __name__ == "__main__":

    # print(client_folder, project_folder)
    print("""
-------------------BEM VINDO AO MENU-------------------
PARA SAIR DO PROGRAMA A QUALQUER MOMENTO APERTE CTRL+C""")
    while True:
        try:
            menu_set()
        except KeyboardInterrupt as err:
            print("\nSaindo do programa")
            break
        except ValueError as err_num:
            print("\nVALOR DIGITADO NÃO É VÁLIDO,RETORNANDO AO MENU PRINCIPAL\n\nPRESSIONE CTRL+C caso deseje encerrar o programa")