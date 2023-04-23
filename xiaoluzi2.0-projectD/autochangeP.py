#auto change power of A,B powersupply
import serial
import serial.tools.list_ports
import time


#input the power_value,auto change power
def ps(powerAs, powerbs, serA, serB):
    Power_A_Setted=powerAs
    Power_B_Setted=powerbs

    #send the right_set_value of Current to powersupply
    def send_settedvalue_to_powersupply(i_a, i_b):
        def powe2():
            serA.write(":VOLT {}\n".format(20).encode('utf-8'))
            serB.write(":VOLT {}\n".format(20).encode('utf-8'))
            serA.write(":CURR {}\n".format(i_a).encode('utf-8'))
            serB.write(":CURR {}\n".format(i_b).encode('utf-8'))
        powe2()
    Calculated_Current_A=4
    Calculated_Current_B=4

    #get the current,volt from powersupply A,B.calculate the Ohm of powersupply,then get the right_set_value of Current
    def ask_value():#output the i
        serA.write(":MEAS:VOLT?\n".encode('utf-8'))
        volt_asked_A_feedback = float(serA.readline()[:-1])
        serB.write(":MEAS:VOLT?\n".encode('utf-8'))
        volt_asked_B_feedback = float(serB.readline()[:-1])
        serA.write(":MEAS:CURR?\n".encode('utf-8'))
        current_asked_A_feedback = float(serA.readline()[:-1])
        serB.write(":MEAS:CURR?\n".encode('utf-8'))
        current_asked_B_feedback = float(serB.readline()[:-1])
        return (volt_asked_A_feedback * current_asked_A_feedback, volt_asked_B_feedback * current_asked_B_feedback, pow(Power_A_Setted / volt_asked_A_feedback * current_asked_A_feedback, 0.5), pow(Power_B_Setted / volt_asked_B_feedback * current_asked_B_feedback, 0.5))
    powerA_feedback, powerB_feedback, Calculated_Current_A, Calculated_Current_B=ask_value()
    if Power_A_Setted<0.1:
        Calculated_Current_A=0.1
    if Power_B_Setted<0.1:
        Calculated_Current_B=0.1#set as 0
    if Calculated_Current_A>6:#set the max i #5
        Calculated_Current_A=6.0
    if Calculated_Current_B>6:
        Calculated_Current_B=6.0
    send_settedvalue_to_powersupply(format(Calculated_Current_A, '.6f'), format(Calculated_Current_B, '.6f'))
    powerA_feedback, powerB_feedback, Calculated_Current_A, Calculated_Current_B=ask_value()


