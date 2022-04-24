from functools import partial
from tkinter import Label, Frame, LEFT, Button, HORIZONTAL, Scale, messagebox, Checkbutton,Radiobutton,IntVar,ALL
#from tkinter import *
import Parameter
import Live_Simulation
from ground_structure import init_constraint_params, init_idm_params
from drawStreetNetwork import drawStreetNetwork


### user interface: on the left of the window
def drawUserInterface(tk, streetNetwork, carDrawer, logger, logger_dict, canvas):

    userInterfaceFrame = Frame(tk, width=Parameter.get_value('userInterfaceFrame_width'), height=Parameter.get_value('Window_Height'))
    userInterfaceFrame.grid(row=0, column=1, padx=20, pady=20)
    header = Label(userInterfaceFrame, text="User Settings",bg='white')
    header.pack(pady=5)


    Button_Frame = Frame(userInterfaceFrame)
    Button_Frame.pack()


    ######################################################################
    ### start: start the simulation
    ### if "control_value" is true, the code simulation of Live_Simulation will run
    def start():
        Parameter.set_value('control_value', True)

        streetNetwork.spawnCar()
        for car in streetNetwork.getAllCars():
            car.updateEnv_And_ValueDict()

        Live_Simulation.simulation(tk, streetNetwork, carDrawer, logger, logger_dict)

    Button_start = Button(Button_Frame, text="start", command=start)
    Button_start.pack(padx=5, side=LEFT)

    ### stop: stop the simulation
    def stop():

        Parameter.set_value('control_value', False)
        Live_Simulation.simulation(tk, streetNetwork, carDrawer, logger, logger_dict)

    Button_stop = Button(Button_Frame, text="stop", command=stop)
    Button_stop.pack(padx=5, side=LEFT)

    ### visible: if the interface is NOT visible, hide it
    ### if interface is NOT visible,the width of center window will be reduced that includes NO Canvas
    def visible():
        if Parameter.get_value('visible'):
            Parameter.set_value('visible', False)
            canvas.grid_remove()
            center_window(tk, Parameter.get_value('userInterfaceFrame_width'), Parameter.get_value('Window_Height'))
        else:
            Parameter.set_value('visible', True)
            canvas.grid(row=0, column=0)
            center_window(tk, Parameter.get_value('Canvas_width') + Parameter.get_value('userInterfaceFrame_width'),
                          Parameter.get_value('Window_Height'))
        Live_Simulation.simulation(tk, streetNetwork, carDrawer, logger, logger_dict)

    Button_visible = Button(Button_Frame, text="visible", command=visible)
    Button_visible.pack(padx=5, side=LEFT)


    ### show street information
    showValue_streetInfo = IntVar()
    showValue_streetInfo.set(1)

    def show_street_info():
        canvas.delete(ALL)
        if showValue_streetInfo.get() == 0:
            Parameter.set_value('show_road_ID', False)
        else:
            Parameter.set_value('show_road_ID', True)
        drawStreetNetwork(canvas, streetNetwork)
        Live_Simulation.simulation(tk, streetNetwork, carDrawer, logger, logger_dict)

    show_street = Checkbutton(userInterfaceFrame, text='Street ID', variable=showValue_streetInfo,
                              command=show_street_info)
    show_street.pack(pady=5)


    ### control speed representation
    showValue_speed = IntVar()
    showValue_speed.set(1)
    def show_bar():
        if showValue_speed.get() == 0:
            Parameter.set_value('show_bar', False)
        else:
            Parameter.set_value('show_bar', True)

    show_bar = Checkbutton(userInterfaceFrame, text='Speed representation', variable=showValue_speed, command=show_bar)
    show_bar.pack(pady=5)


    flowsetting = Label(userInterfaceFrame, text="Flow Settings", bg='white')
    flowsetting.pack(pady=5)
    ### inflow control: determine how many cars per hour flow into network
    def set_inflow(event):
        ### show the current inflow
        inflow_Label.config(text='Current flow is ' + str(inflow.get()) + ' veh/h.')
        if inflow.get() is not 0:
            Parameter.set_value('spawnNewCarLimit', 36000 / inflow.get())
        else:
            Parameter.set_value('spawnNewCarLimit', 10000)

    inflow_Label = Label(userInterfaceFrame, width=30,
                        text='Current Inflow of cars is: ' + '1000' + ' veh/h.')
    inflow_Label.pack(pady=5)
    inflow = Scale(userInterfaceFrame, label='Inflow', from_=0, to=4000, orient=HORIZONTAL,
                                   length=275, showvalue=0,
                                   tickinterval=1000, resolution=1)
    ### initial value of the inflow
    inflow.set(1000)
    inflow.bind('<ButtonRelease-1>', set_inflow)
    inflow.pack(pady=5)


    # Custom probability settings
    Label(userInterfaceFrame, text="Customizable Nodes Settings",bg='white').pack(pady=5)
    Label(userInterfaceFrame, text="Set probability weights for each node below.").pack(pady=5)
    nodeFrame = Frame(userInterfaceFrame, padx=20, pady=20)
    nodeFrame.pack(pady=5)
    nodes = streetNetwork.getAllNodesWhereProbabilityCanBeCustomized()
    if nodes:
    ### the node which can be control is green
        for node in nodes:
            subNodeFrame = Frame(userInterfaceFrame, padx=20, pady=20)
            subNodeFrame.pack()
            Label(subNodeFrame, text=['Node:',node.id], bg="Sea Green1").grid(row=1, column=0)

            scales = []
            j = 1

            for outgoingStreet in node.outgoingStreets:
                Label(subNodeFrame, text=['Street:',outgoingStreet.id], fg="red").grid(row=0, column=j+1)
                scale = Scale(subNodeFrame, from_=0, to=100,
                      orient=HORIZONTAL)
                scale.grid(row=1, column=j+1)
                scales.append(scale)
                j += 1

            safeSettingsAction = partial(saveNodeProbabilities, node, scales)
            Button(subNodeFrame, text="Apply", command=safeSettingsAction).grid(row=2, column=0)


    ### select the drive mode and use the noise or not
    l0 = Label(userInterfaceFrame, text='Driving Modes Settings',bg='white')
    l0.pack(pady=5)
    l1 = Label(userInterfaceFrame, text='Car will run in idm Mode without Gaussian noise')
    l1.pack(pady=5)
    var1 = IntVar()
    var1.set(1)
    var2 = IntVar()
    var2.set(0)

    def car_mode():
        #choose the different drive modes
        if var1.get() == 1:
            mode_name = 'idm'
        if var1.get() == 2:
            mode_name = 'ext_idm'
        if var1.get() == 3:
            mode_name = 'lim_idm'
        if var1.get() == 4:
            mode_name = 'lim_idm+'
        # use noise or not
        if var2.get() == 0:
            noise_or_not = ' without '
        if var2.get() == 1:
            noise_or_not = ' with '

        print('You have selected the ' + mode_name + ' mode'+ noise_or_not +'noise')
        l1.config(text='Car will run in ' + mode_name + ' Mode'+ noise_or_not +'Gaussian noise')

        # change or update the drive mode and noise mode of the car in the streets
        for car in streetNetwork.getAllCars():
            car.idm_params['advance_mode'] = mode_name
            car.idm_params['noise_mode'] = var2.get()

        # change or update the drive mode and noise mode of the new car
        idm_params = Parameter.get_value('idm_params')
        for i in range(len(idm_params)):
            idm_params[i]['advance_mode'] = mode_name
            idm_params[i]['noise_mode'] = var2.get()
        Parameter.set_value('idm_params', idm_params)

        Live_Simulation.simulation(tk, streetNetwork, carDrawer, logger, logger_dict)

    modeFrame = Frame(userInterfaceFrame, padx=20, pady=10)
    modeFrame.pack(pady=5)

    Radiobutton(modeFrame, variable=var1, text="        idm      ", value=1, command=car_mode, indicatoron=False).grid(row=0, column=0)
    Radiobutton(modeFrame, variable=var1, text="    ext_idm    ", value=2, command=car_mode, indicatoron=False).grid(row=0, column=1)
    Radiobutton(modeFrame, variable=var1, text="    lim_idm    ", value=3, command=car_mode, indicatoron=False).grid(row=1, column=0)
    Radiobutton(modeFrame, variable=var1, text="   lim_idm+   ", value=4, command=car_mode, indicatoron=False).grid(row=1, column=1)

    l2 = Label(modeFrame, text='            ').grid(row=2, column=1)
    Checkbutton(modeFrame, variable=var2, text=" Gaussian noise ", command=car_mode).grid(row=3, column=0)




#############################################################################################################

## save the turn probability in node
def saveNodeProbabilities(node, scales):
    probabilities=[]
    for scale in scales:
        probabilities.append(scale.get())

    result = True
    i = probabilities.count(0)
    if i == 1:
        result = messagebox.askokcancel(title='Warning', message='One probability is set to 0. Are you sure to proceed?')
    if result:
        node.setProbabilities(probabilities)
        node.ischanged = True
        print("Node probabilities saved for " + str(node.id))


# makes the animation windows on the center
def center_window(root, w, h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

###################################################################################################################










