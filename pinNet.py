#/usr/bin/python3
from datetime import datetime
import threading
import subprocess
import IpCalc
import os
import sys
import re

#список потоков
tread_list = []
thread_list_mac = []
data_addr = []
data_mac = []
#Метод Ping отправка icmp
def pin(addr):
    for i in range(4):
         addr[i] = str(addr[i])
    ip_addr = '.'.join(addr)
    p = subprocess.Popen(['ping','-c','4', ip_addr], stdout=subprocess.DEVNULL)
    p.wait()
    global data_addr
    if not p.poll():
        print("is up {0}".format(ip_addr))
        data_addr.append("is up {0}".format(ip_addr))
#Метод Arp запрос
def arp(addr):
        addr = addr.split(' ')
        subprocess.Popen(['ping','-c','4', addr[2]], stdout=subprocess.DEVNULL).wait()
        pid = subprocess.Popen(['arp','-n', addr[2]], stdout=subprocess.PIPE)
        s = pid.communicate()[0]
        result = str(s).split(' ')
        for i in result:
                tes = re.match(r".{2}:.{2}:.{2}:.{2}:.{2}:.{2}",i)
                if tes:
                   global data_mac        
                   print("is up IP:{0}, MAC->{1}".format(addr[2], i))
                   data_mac.append("is up IP:{0}, MAC->{1}".format(addr[2], i))

#Создание потоков
def createThread(count, ls_ip):
        for i in range(count):
                t = threading.Thread(target=pin, name="thr{0}".format(i), args=(ls_ip[i],))
                tread_list.append(t)
                t.start()
        for th in tread_list:
                th.join()
#Метод выполняет запуск пингов в отдельных потоках
def running(count_thread, list_ip):
        #счетчик заполнение ip адресов
        sw = 0
        #список ip адресов
        list_addr = []
        #Получим текущее кол-во оставшихся адресов
        currentAddr = len(list_ip)
        exit = True
        i = 0
        while exit:
                #Выполняем тогда когда заполниться список list_addr, sw - счетчик заполнения
                if sw == count_thread:
                        sw = 0
                        #Каждый адрес выполняется в отдельном потоке
                        createThread(count_thread, list_addr)
                        #После список очищаем для последущего пополнения
                        list_addr.clear()
                        #Это операция нужна для того чтобы узнать кол-во оставшихся адресов
                        currentAddr = currentAddr - count_thread
                        #Проверяем если список адресов меньше чем кол-во запрошеных потоков
                        if currentAddr <= count_thread:
                                #Выполняем данные операции для того чтоб определить сколько потоков нужно для оставшихся адресов
                                result = count_thread - currentAddr
                                if result > currentAddr:
                                         count_thread = currentAddr
                                else:
                                        count_thread = currentAddr - result
                try:
                    list_addr.append(list_ip[i])
                except IndexError:
                        exit = False
                sw = sw + 1
                i = i + 1
#Узнаем mac-адрес устройства
def query_mac_address(addr):
        for i in range(len(addr)):
             thr = threading.Thread(target=arp, name="th_arp{0}".format(i), args=(addr[i],))
             thread_list_mac.append(thr)
             thr.start()
        for th in thread_list_mac:
                th.join()

def init(ip_min, ip_max):
    #Отсчет октетат начинаем с конца
    octet = 3
    #храним ip адреса
    data = []
    #данная переменная служит для результата равны ли все октеты
    result = 0
    #вход в цикл
    input = True 
    for i in range(4):
        ip_min[i] = int(ip_min[i])
        ip_max[i] = int(ip_max[i])
    #нужна для изменения адреса
    min = ip_min
    num = ip_min[octet]
    #Тут увеличиваем адреса до заданого ip адреса
    while input:
        #последний октет, также строка octet -= 1 служит 
        # для сброса чтобы начать заполнять с конца октета адреса
        if octet == 3:
            while num <= ip_max[octet]:
                min[octet] = num
                data.append(list(min))   
                #увеличиваем на один адрес    
                num += 1
            num = 0                
        elif octet == 2:
            if ip_min[octet] <= ip_max[octet]:
                min[octet] += 1
                min[3] = 0
                octet = -1
        elif octet == 1:
            if ip_min[octet] <= ip_max[octet]:
                min[octet] += 1
                min[3] = 0
                min[2] = 0
                octet = -1
        elif octet == 0:
            if ip_min[octet] <= ip_max[octet]:
                min[octet] += 1
                min[3] = 0
                min[2] = 0
                min[1] = 0
                octet = -1
        #функция вызова асинхрон пинг
        running(int(res_args[3]), data)
        #Проверяем равен ли миниальный адрес с максимальным чтобы узнать все адреса просмотрели
        for i in range(4):
            if ip_min[i] == ip_max[i]:
                result+=1
            else:
                result = 0
        if result == 4:
            #Выход из цикла
            input = False
        if octet >= 0:    
            octet -= 1
        else:
            octet = 3 
        data.clear()          

res_args = sys.argv

ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",res_args[1])
mask = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", res_args[2])
if ip and mask:
   res = IpCalc.IpCalc("".join(res_args[1]), "".join(res_args[2]))
   print("Searching for active ip addresses!\n")
   init(res.minAddr(), res.maxAddr())
        #Условие для того чтобы узнать нужен ли нам mac адрес
   try:
        if res_args[4] == 'arp':
            query_mac_address(data_addr)
   except IndexError:
        print("Output without arp!")
else:
       print("No good format!")

#Текущее время
today = datetime.today()
result_today = "{0} {1}".format(today.strftime("%H:%M:%S"), today.strftime("%d-%m-%Y"))
#Проверяем сущ файл или нет, если да тогда дописываем, если нет создаем новый файл для записей
if os.path.exists('log.txt'):
    #Выполняем до запись файла
    file = open('log.txt','a')
    file.write(result_today + '\n')
    try:
        if res_args[4] == "arp":
                for rData in data_mac:      
                       file.write(rData + '\n')         
    except IndexError:
            for rData in data_addr:      
               file.write(rData + '\n')
    file.close()
else:
    #Создаем файл
    file = open('log.txt','w')
    file.write(result_today + '\n')
    try:
        if res_args[4] == "arp":
                for rData in data_mac:      
                       file.write(rData + '\n')         
    except IndexError:
        for rData in data_addr:      
            file.write(rData + '\n')
    file.close()
