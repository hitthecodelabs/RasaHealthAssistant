import os
import json
import time
import numpy as np
from glob import glob

# print(glob("*"))

from typing import Text, Dict, Any, List

import psycopg2
from difflib import SequenceMatcher
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class CustomGreetingAction(Action):
    def name(self) -> Text:
        return "action_get_logged_in_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(glob("*"))
        
        f = open('../../temp/temp.json')
        data = json.load(f)
        print(data)
        username = data['username']
        fname = data['first_name']
        sname = data['last_name']
        u_type = ''
        if data['user_type']=='doctor':
            u_type = ' Dr.'

        screen_name = ''
        if fname!='' and sname!='':
            # screen_name += f'{fname} {sname}'.strip().title()
            screen_name += f'{fname}'.strip().title()
        elif fname!='' and sname=='':
            screen_name += f'{fname}'.strip().title()
        elif fname=='' and sname!='':
            screen_name += f'{sname}'.strip().title()
        elif fname=='' and sname=='':
            screen_name += f'{username}'
        
        # Modify the greeting message to include the username
        message = f"¡Hola{u_type} {screen_name}! ¿En qué puedo ayudarle el día de hoy?"
        
        # Send the modified greeting message back to the user
        dispatcher.utter_message(text=message)
        
        return []

class CustomMenuAction(Action):
    def name(self) -> Text:
        return "action_detectar_consulta"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        f = open('../../temp/temp.json')
        data = json.load(f)
        message = ''
        if data['user_type']=='doctor':        
            message = f"Por favor, selecciona el tipo de consulta que deseas realizar:\n1. Pacientes\n2. Rutinas prescritas\n3. Trazabilidad de pacientes"
        else:
            message = f"Por favor, selecciona el tipo de consulta que deseas realizar:\n1. Historial clínico\n2. Rutinas y ejercicio físico\n3. Trazabilidad"
        
        # Send the modified greeting message back to the user
        dispatcher.utter_message(text=message)
        
        return []

class CustomMedicoPacientes(Action):
    def name(self) -> Text:
        return "action_consulta_medico_pacientes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        envs = glob("../../.e*v")
        A = open(envs[0], "r")
        S = {i.split("=")[0]:i.split("=")[-1].strip().replace('"', "") 
             for i in A.readlines() 
             if ((i.strip()!='')&("=" in i))}
        A.close()
        
        # Conéctate a la base de datos
        conn = psycopg2.connect(
            host=S['DATABASE_HOST'],
            database=S['POSTGRES_DB'],
            user=S['POSTGRES_USER'],
            password=S['POSTGRES_PASSWORD']
        )
        
        # POSTGRES_USER=postgres
        # POSTGRES_PASSWORD=""
        # POSTGRES_DB=rasa
        # DATABASE_HOST=localhost
        
        # Crear un cursor para ejecutar las sentencias SQL
        cur = conn.cursor()
        
        # Ejecuta una consulta SQL para obtener todos los usuarios
        cur.execute("SELECT * FROM users_alluser")
        
        pacientes = []
        # Recorre todos los registros devueltos por la consulta
        for row in cur.fetchall():
            # Imprime los datos de cada usuario
            # print(row)
            # print()
            phrase = ''
            if "doctor" not in row:
                usuario, nombre, apellido, correo = row[4:8]
                phrase += f"Nombre: {nombre}  {apellido}\n"
                phrase += f"Usuario: {usuario}\n"
                phrase += f"Correo: {correo}"
                pacientes.append(phrase)
        
        # Cierra el cursor
        cur.close()
        # Cierra la conexión
        conn.close()
        f = open('../../temp/temp.json')
        data = json.load(f)
        
        if data['user_type']=='doctor' and len(pacientes)>0:
            pacientes.append("¿Desea realizar otra consulta?")
            message = "\n\n".join(pacientes)
        else:
            message = "Actualmente no mantiene historial con pacientes. ¿Desea realizar otra consulta?"
        
        # Send the modified greeting message back to the user
        dispatcher.utter_message(text=message)
        
        return []

class CustomMedicoTrazabilidad(Action):
    def name(self) -> Text:
        return "action_consulta_medico_appointments"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        envs = glob("../../.e*v")
        A = open(envs[0], "r")
        S = {i.split("=")[0]:i.split("=")[-1].strip().replace('"', "") 
             for i in A.readlines() 
             if ((i.strip()!='')&("=" in i))}
        A.close()
        
        # Conéctate a la base de datos
        conn = psycopg2.connect(
            host=S['DATABASE_HOST'],
            database=S['POSTGRES_DB'],
            user=S['POSTGRES_USER'],
            password=S['POSTGRES_PASSWORD']
        )

        # Crea un cursor para ejecutar las sentencias SQL
        cur = conn.cursor()

        # Ejecuta una consulta SQL para obtener todos los usuarios
        cur.execute("SELECT * FROM appointments_appointment")

        # Recorre todos los registros devueltos por la consulta
        D = {}
        for row in cur.fetchall():
            # Imprime los datos de cada usuario
            # print(row)
            date_ = row[2]
            hour_ = row[5]
            user_index = row[4]
            patient_id = row[1]
            appointment_date = row[2].strftime("%Y-%m-%d") + " " + row[5].strftime("%H:%M:%S")

            if user_index not in D:
                D[user_index] = [[patient_id, appointment_date]]
            else:
                D[user_index].append([patient_id, appointment_date])

        # Cierra el cursor
        cur.close()

        # Crea un cursor para ejecutar las sentencias SQL
        cur = conn.cursor()

        # Ejecuta una consulta SQL para obtener todos los usuarios
        cur.execute("SELECT * FROM users_alluser")

        P = {}
        # Recorre todos los registros devueltos por la consulta
        for row in cur.fetchall():
            # Imprime los datos de cada usuario
            # print(row)
            # print()
            phrase = ''
            if "doctor" not in row:
                usuario, nombre, apellido, correo = row[4:8]
                u_id = row[0]
                if u_id not in P:
                    P[u_id] = [usuario, nombre, apellido, correo]

        # Cierra el cursor
        cur.close()
        conn.close()

        ss = []
        for u_id in P:
            usuario, nombre, apellido, correo = P[u_id]
            if u_id in D:
                dates = D[u_id]
                for cedula, fecha in dates:
                    string = f"Fecha: {fecha}\nPaciente: {nombre} {apellido}\nCédula: {cedula}"
                    ss.append(string)
        
        if len(ss)>0:
            ss.append("¿Desea realizar otra consulta?")
            mensaje = "\n\n".join(ss)
        else:
            mensaje = "Actualmente no mantiene pacientes para su trazabilidad. ¿Desea realizar otra consulta?"
        # print(mensaje)
        
        # Send the modified greeting message back to the user
        dispatcher.utter_message(text=mensaje)
        
        return []

class CustomMedicoRutinas(Action):
    def name(self) -> Text:
        return "action_consulta_medico_rutinas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        f = open('../../temp/temp.json')
        data = json.load(f)
        print(data)
        username = data['username']
        
        envs = glob("../../.e*v")
        A = open(envs[0], "r")
        S = {i.split("=")[0]:i.split("=")[-1].strip().replace('"', "") 
             for i in A.readlines() 
             if ((i.strip()!='')&("=" in i))}
        A.close()
        
        # Conéctate a la base de datos
        conn = psycopg2.connect(
            host=S['DATABASE_HOST'],
            database=S['POSTGRES_DB'],
            user=S['POSTGRES_USER'],
            password=S['POSTGRES_PASSWORD']
        )
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM users_alluser")
        ps_l, c_appos, c_pc = [], [], []
        for row in cur.fetchall():ps_l.append([row[0]] + list(row[4:8]) + list(row[-2:]))
        cur.close()
        cur = conn.cursor()
        cur.execute("SELECT * FROM appointments_appointment")
        for row in cur.fetchall():
            if type(row[-1])==int:c_appos.append(row)
        cur.close()
        cur = conn.cursor()
        cur.execute("SELECT * FROM appointments_prescription")
        for row in cur.fetchall():c_pc.append(row)
        cur.close()
        conn.close()

        A = {}
        B = {}
        for appo in c_appos:
            fecha = appo[2].strftime("%Y-%m-%d") + ' ' + appo[5].strftime("%H:%M:%S")
            pat_id, appo_id, pc_l, doc_l = appo[4], appo[-1], [], []
            for pc in c_pc:
                if appo_id==pc[0]:pc_l+=pc[1:]
            for user in ps_l:
                if pc_l[-1]==user[0]:doc_l+=user[1:]
            for u_l in ps_l:
                if pat_id in u_l:
                    if pat_id not in A:A[u_l[1]] = [u_l[1:] + [fecha] + pc_l[:-1] + doc_l]
                    else:A[u_l[1]] += [u_l[1:] + [fecha] + pc_l[:-1] + doc_l]
                    if doc_l[0] not in B:B[doc_l[0]] = [u_l[1:] + [fecha] + pc_l[:-1] + doc_l]
                    else:B[doc_l[0]] += [u_l[1:] + [fecha] + pc_l[:-1] + doc_l]
        print(A)
        print(B)
        
        dd = B[username]

        mensaje = ''
        for info in dd:
            nombre = info[1]
            apellido = info[2]
            cedula = info[4]
            fecha = info[6]
            prescripcion = info[7]
            descripcion = info[8]

            if prescripcion!='':
                formato = f"""Paciente: {nombre} {apellido}\nCedula: {cedula}\nFecha consulta: {fecha}\nPrescripcion: {prescripcion}\nDescripcion: {descripcion}\n\n"""
                mensaje+=formato
        
        if len(mensaje)==0:
            mensaje = "Actualmente no tiene citas médicas en su historial. ¿Desea realizar otra consulta?"
        
        # Send the modified greeting message back to the user
        dispatcher.utter_message(text=mensaje)
        dispatcher.utter_message(text="¿Desea realizar otra consulta?")
        
        return []

class CustomPacienteHistorial(Action):
    def name(self) -> Text:
        return "action_consulta_paciente_appointments"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        envs = glob("../../.e*v")
        A = open(envs[0], "r")
        S = {i.split("=")[0]:i.split("=")[-1].strip().replace('"', "") 
             for i in A.readlines() 
             if ((i.strip()!='')&("=" in i))}
        A.close()
        
        # Conéctate a la base de datos
        conn = psycopg2.connect(
            host=S['DATABASE_HOST'],
            database=S['POSTGRES_DB'],
            user=S['POSTGRES_USER'],
            password=S['POSTGRES_PASSWORD']
        )
        
        f = open('../../temp/temp.json')
        data = json.load(f)
        print(data)
        username = data['username']

        # Crea un cursor para ejecutar las sentencias SQL
        cur = conn.cursor()

        # Ejecuta una consulta SQL para obtener todos los usuarios
        cur.execute("SELECT * FROM appointments_appointment")

        # Recorre todos los registros devueltos por la consulta
        D = {}
        for row in cur.fetchall():
            # Imprime los datos de cada usuario
            # print(row)
            date_ = row[2]
            hour_ = row[5]
            user_index = row[4]
            patient_id = row[1]
            appointment_date = row[2].strftime("%Y-%m-%d") + " " + row[5].strftime("%H:%M:%S")

            if user_index not in D:
                D[user_index] = [[patient_id, appointment_date]]
            else:
                D[user_index].append([patient_id, appointment_date])

        # Cierra el cursor
        cur.close()

        # Crea un cursor para ejecutar las sentencias SQL
        cur = conn.cursor()

        # Ejecuta una consulta SQL para obtener todos los usuarios
        cur.execute("SELECT * FROM users_alluser")

        P = {}
        # Recorre todos los registros devueltos por la consulta
        for row in cur.fetchall():
            # Imprime los datos de cada usuario
            # print(row)
            # print()
            phrase = ''
            if username in row:
                usuario, nombre, apellido, correo = row[4:8]
                u_id = row[0]
                if u_id not in P:
                    P[u_id] = [usuario, nombre, apellido, correo]

        # Cierra el cursor
        cur.close()
        conn.close()

        ss = []
        for u_id in P:
            usuario, nombre, apellido, correo = P[u_id]
            if u_id in D:
                dates = D[u_id]
                for cedula, fecha in dates:
                    string = f"Fecha de la cita médica: {fecha}"
                    ss.append(string)
        
        if len(ss)>0:
            ss.append("¿Desea realizar otra consulta?")
            mensaje = "\n\n".join(ss)
            # print(mensaje)
        else:
            mensaje = "Actualmente no tiene citas médicas en su historial. ¿Desea realizar otra consulta?"
        
        # Send the modified greeting message back to the user
        dispatcher.utter_message(text=mensaje)
        
        return []

class CustomPacienteTrazabilidad(Action):
    def name(self) -> Text:
        return "action_consulta_paciente_trazabilidad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        f = open('../../temp/temp.json')
        data = json.load(f)
        print(data)
        username = data['username']
        
        envs = glob("../../.e*v")
        A = open(envs[0], "r")
        S = {i.split("=")[0]:i.split("=")[-1].strip().replace('"', "") 
             for i in A.readlines() 
             if ((i.strip()!='')&("=" in i))}
        A.close()
        
        # Conéctate a la base de datos
        conn = psycopg2.connect(
            host=S['DATABASE_HOST'],
            database=S['POSTGRES_DB'],
            user=S['POSTGRES_USER'],
            password=S['POSTGRES_PASSWORD']
        )
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM users_alluser")
        ps_l, c_appos, c_pc = [], [], []
        for row in cur.fetchall():ps_l.append([row[0]] + list(row[4:8]) + list(row[-2:]))
        cur.close()
        cur = conn.cursor()
        cur.execute("SELECT * FROM appointments_appointment")
        for row in cur.fetchall():
            if type(row[-1])==int:c_appos.append(row)
        cur.close()
        cur = conn.cursor()
        cur.execute("SELECT * FROM appointments_prescription")
        for row in cur.fetchall():c_pc.append(row)
        cur.close()
        conn.close()

        A = {}
        B = {}
        for appo in c_appos:
            fecha = appo[2].strftime("%Y-%m-%d") + ' ' + appo[5].strftime("%H:%M:%S")
            pat_id, appo_id, pc_l, doc_l = appo[4], appo[-1], [], []
            for pc in c_pc:
                if appo_id==pc[0]:pc_l+=pc[1:]
            for user in ps_l:
                if pc_l[-1]==user[0]:doc_l+=user[1:]
            for u_l in ps_l:
                if pat_id in u_l:
                    if pat_id not in A:A[u_l[1]] = [u_l[1:] + [fecha] + pc_l[:-1] + doc_l]
                    else:A[u_l[1]] += [u_l[1:] + [fecha] + pc_l[:-1] + doc_l]
                    if doc_l[0] not in B:B[doc_l[0]] = [u_l[1:] + [fecha] + pc_l[:-1] + doc_l]
                    else:B[doc_l[0]] += [u_l[1:] + [fecha] + pc_l[:-1] + doc_l]
                        
        dd = A[username]

        mensaje = ''
        for info in dd:
            doctor = info[-6]
            doctor_ced = info[-2]
            apellido = info[2]
            cedula = info[4]
            fecha = info[6]
            prescripcion = info[7]
            description = info[8]

            if prescripcion!='':
                formato = f"""Doctor: {doctor}\nCedula: {doctor_ced}\nFecha consulta: {fecha}\nPrescripcion: {prescripcion}\nDescripcion: {description}\n\n¿Desea realizar otra consulta?"""
                mensaje+=formato
        
        if len(mensaje)==0:
            mensaje = "Actualmente no tiene citas médicas en su historial. ¿Desea realizar otra consulta?"
        
        # Send the modified greeting message back to the user
        dispatcher.utter_message(text=mensaje)
        
        return []

class CustomPacienteRutina(Action):
    def name(self) -> Text:
        return "action_consulta_paciente_rutinas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        f = open('../../temp/temp.json')
        data = json.load(f)
        print(data)
        username = data['username']
        
        envs = glob("../../.e*v")
        A = open(envs[0], "r")
        S = {i.split("=")[0]:i.split("=")[-1].strip().replace('"', "") 
             for i in A.readlines() 
             if ((i.strip()!='')&("=" in i))}
        A.close()
        
        # Conéctate a la base de datos
        conn = psycopg2.connect(
            host=S['DATABASE_HOST'],
            database=S['POSTGRES_DB'],
            user=S['POSTGRES_USER'],
            password=S['POSTGRES_PASSWORD']
        )
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM users_alluser")
        ps_l, c_appos, c_pc = [], [], []
        for row in cur.fetchall():ps_l.append([row[0]] + list(row[4:8]) + list(row[-2:]))
        cur.close()
        cur = conn.cursor()
        cur.execute("SELECT * FROM appointments_appointment")
        for row in cur.fetchall():
            if type(row[-1])==int:c_appos.append(row)
        cur.close()
        cur = conn.cursor()
        cur.execute("SELECT * FROM appointments_prescription")
        for row in cur.fetchall():c_pc.append(row)
        cur.close()
        conn.close()

        A = {}
        B = {}
        for appo in c_appos:
            fecha = appo[2].strftime("%Y-%m-%d") + ' ' + appo[5].strftime("%H:%M:%S")
            pat_id, appo_id, pc_l, doc_l = appo[4], appo[-1], [], []
            for pc in c_pc:
                if appo_id==pc[0]:pc_l+=pc[1:]
            for user in ps_l:
                if pc_l[-1]==user[0]:doc_l+=user[1:]
            for u_l in ps_l:
                if pat_id in u_l:
                    if pat_id not in A:A[u_l[1]] = [u_l[1:] + [fecha] + pc_l[:-1] + doc_l]
                    else:A[u_l[1]] += [u_l[1:] + [fecha] + pc_l[:-1] + doc_l]
                    if doc_l[0] not in B:B[doc_l[0]] = [u_l[1:] + [fecha] + pc_l[:-1] + doc_l]
                    else:B[doc_l[0]] += [u_l[1:] + [fecha] + pc_l[:-1] + doc_l]
                        
        dd = A[username]

        prescritas = []
        rutinas_predef = ['flexiones', 'caminata', 'trote', "barras"]
        for info in dd:
            prescripcion = info[7]
            description = info[8]
            
            for rut in rutinas_predef:
                similaridad = SequenceMatcher(None, rut, prescripcion).ratio()
                if similaridad>=0.70:
                    prescritas.append([rut, prescripcion, description, similaridad])
        
        print(glob("*/*"))
        print(prescritas)
        for presc in prescritas:
            
            if presc[0]=='flexiones':
                # dispatcher.utter_message(attachment="imgs/flexiones.png")
                dispatcher.utter_message(image="https://i.imgur.com/YNc01t8.png")
                dispatcher.utter_message(text=presc[2])
                dispatcher.utter_message(text="¿Desea realizar otra consulta?")
            elif presc[0]=='caminata':
                # dispatcher.utter_message(attachment="imgs/caminata.png")
                dispatcher.utter_message(image="https://i.imgur.com/OS9n7Fq.png")
                dispatcher.utter_message(text=presc[2])
                dispatcher.utter_message(text="¿Desea realizar otra consulta?")
            elif presc[0]=='trote':
                # dispatcher.utter_message(attachment="imgs/trote.png")
                dispatcher.utter_message(image="https://i.imgur.com/jUaxTKT.png")
                dispatcher.utter_message(text=presc[2])
                dispatcher.utter_message(text="¿Desea realizar otra consulta?")
                
        
        if len(prescritas)==0:
            mensaje = "Actualmente no tiene rutinas prescritas en su historial. ¿Desea realizar otra consulta?"
            dispatcher.utter_message(text=mensaje)
        
        return []

