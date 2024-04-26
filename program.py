import os
import env as path
import datetime as dt
from handle_json import *

def prompt_clients(list_clients_b=True):
    list_clients = os.listdir(path.PATTERN_PATH) if list_clients_b == True else list_clients_b 
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
    if clients_texted == '':
        return print('Não há pastas neste diretorio')
    return clients_dict

def rename_alias(verify=True):
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
        app_obj = {clients_dict.get(int(selected_client)) : set_alias}
        update_file(app_obj, 'client_alias.json')


def set_folder():
    """a function that recognizes the inputs given and creates a folder on the specified path
    """
    clients_dict = prompt_clients()
    while True:
        selected_client = input("Selecione o número correspondente ao cliente desejado: ")
        if clients_dict.get(int(selected_client)) != None:
            print(f"\nVocê selecionou o cliente : {clients_dict.get(int(selected_client))}")
        break
        
    job_num = input("\nInsira o número do job: ").replace(' ' , '')
    job_name = input("\nInsira o nome do job: ").replace(' ' , '').lower()
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

    job_concat = f"{date_vl}_JOB{job_num}_{job_name}"
    dir_validate = input(f"O nome do job é {job_concat}, aperte 'N' se deseja recomeçar: ")
    if dir_validate.lower() == 'n':
        set_folder()
    os.chdir(path.PATTERN_PATH + '/' + clients_dict.get((int(selected_client))))
    os.mkdir(job_concat)
    os.chdir(job_concat)
    os.mkdir('in')
    os.mkdir('out')

def menu_set():
    rename_alias()
    given_option = int(input("""
    O que gostaria de fazer?
    1. Criar uma pasta para um projeto
    2. Dê um apelido para uma pasta de um cliente
    selecione o número correspondente: """))
    if given_option == 1:
        set_folder()
    elif given_option == 2:
        rename_alias(False)
    else:
        given_option = int(input("não identifiquei a sua escolha, por favor escolha novamente"))
        menu_set()

if __name__ == "__main__":
    print("""
-------------------BEM VINDO AO MENU-------------------
PARA SAIR DO PROGRAMA A QUALQUER MOMENTO APERTE CTRL+C""")
    try:
        menu_set()
    except KeyboardInterrupt as err:
        print("\nSaindo do programa")