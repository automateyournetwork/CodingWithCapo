import json
import logging
import time
from pyats import aetest
from pyats.log.utils import banner
from rich.console import Console
from rich.table import Table

## Get Logger 

log = logging.getLogger(__name__)

MAX_RETRIES = 3

## AE TEST SETUP

class common_setup(aetest.CommonSetup):
    """Common Setup Section"""
    #Connect to testbed
    @aetest.subsection
    def connect_to_devices(self,testbed):
        testbed.connect()

    @aetest.subsection
    def loop_mark(self,testbed):
        aetest.loop.mark(Test_Interfaces, device_name=testbed.devices)

class Test_Interfaces(aetest.Testcase):
    """Learn interface tests from pyATS"""
    @aetest.test
    def setup(self,testbed,device_name):
        self.device = testbed.devices[device_name]

    @aetest.test
    def capture_interface_state(self):
        self.parsed_interfaces = self.device.learn("interface")

    @aetest.test
    def write_to_file(self):
        #create a json file of the interface data
        with open(f'{self.device.alias}_pyATS_Learn_Interface.json', 'w') as f:
            f.write(json.dumps(self.parsed_interfaces.info, indent=4, sort_keys=True))

    @aetest.test
    def test_interface_input_crc_errors(self):
        input_crc_error_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input CRC Errors")
        table.add_column("Device", style="blue")
        table.add_column("Interface", style="magenta")
        table.add_column("Input CRC Error Threshold", style="green")
        table.add_column("Input CRC Errors", style="red")
        table.add_column("Passed/Failed", style="yellow")
        for self.intf,value in self.parsed_interfaces.info.items():
            if 'in_crc_errors' in value['counters']:
                counter = value['counters']['in_crc_errors']
                if int(counter) > input_crc_error_threshold:
                    table.add_row(self.device.alias,self.intf,str(input_crc_error_threshold),str(counter),'FAILED',style='red')
                    self.failed_interfaces = "failed"
                else:
                    table.add_row(self.device.alias,self.intf,str(input_crc_error_threshold),str(counter),'PASSED',style='green')
        
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table)

        log.info(capture.get())

        # Should we pass or faile the test?
        if self.failed_interfaces:
            self.failed("Some interfaces have failed the Input CRC Test")
        else:
            self.passed("No interfaces have any Input CRC Errors")

    @aetest.test
    def test_interface_input_errors(self):
        input_error_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input Errors")
        table.add_column("Device", style="blue")
        table.add_column("Interface", style="magenta")
        table.add_column("Input Error Threshold", style="green")
        table.add_column("Input Errors", style="red")
        table.add_column("Passed/Failed", style="yellow")
        for self.intf,value in self.parsed_interfaces.info.items():
            if 'in_errors' in value['counters']:
                counter = value['counters']['in_errors']
                if int(counter) > input_error_threshold:
                    table.add_row(self.device.alias,self.intf,str(input_error_threshold),str(counter),'FAILED',style='red')
                    self.failed_interfaces = "failed"
                else:
                    table.add_row(self.device.alias,self.intf,str(input_error_threshold),str(counter),'PASSED',style='green')
        
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table)

        log.info(capture.get())

        # Should we pass or faile the test?
        if self.failed_interfaces:
            self.failed("Some interfaces have failed the Input Error Test")
        else:
            self.passed("No interfaces have any Input Errors")

    @aetest.test
    def test_interface_output_errors(self):
        output_error_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Output Errors")
        table.add_column("Device", style="blue")
        table.add_column("Interface", style="magenta")
        table.add_column("Output Error Threshold", style="green")
        table.add_column("Output Errors", style="red")
        table.add_column("Passed/Failed", style="yellow")
        for self.intf,value in self.parsed_interfaces.info.items():
            if 'out_errors' in value['counters']:
                counter = value['counters']['out_errors']
                if int(counter) > output_error_threshold:
                    table.add_row(self.device.alias,self.intf,str(output_error_threshold),str(counter),'FAILED',style='red')
                    self.failed_interfaces = "failed"
                else:
                    table.add_row(self.device.alias,self.intf,str(output_error_threshold),str(counter),'PASSED',style='green')
        
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table)

        log.info(capture.get())

        # Should we pass or faile the test?
        if self.failed_interfaces:
            self.failed("Some interfaces have failed the Output Error Test")
        else:
            self.passed("No interfaces have any Output Errors")

    @aetest.test
    def test_interface_duplex(self):
        duplex_threshold = "full"
        self.failed_interfaces = {}
        table = Table(title="Interface Duplex Mode")
        table.add_column("Device", style="blue")
        table.add_column("Interface", style="magenta")
        table.add_column("Duplex Mode Threshold", style="green")
        table.add_column("Duplex Mode", style="red")
        table.add_column("Passed/Failed", style="yellow")
        for self.intf,value in self.parsed_interfaces.info.items():
            if 'duplex_mode' in value:
                counter = value['duplex_mode']
                if counter != duplex_threshold:
                    table.add_row(self.device.alias,self.intf,str(duplex_threshold),str(counter),'FAILED',style='red')
                    self.failed_interfaces = "failed"
                else:
                    table.add_row(self.device.alias,self.intf,str(duplex_threshold),str(counter),'PASSED',style='green')
        
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table)

        log.info(capture.get())

        # Should we pass or faile the test?
        if self.failed_interfaces:
            self.failed("Some interfaces are not full duplex")
        else:
            self.passed("All interfaces are full duplex")

    @aetest.test
    def test_interface_oper_status(self):
        oper_status_threshold = "up"
        self.failed_interfaces = {}
        table = Table(title="Interface Operational Status")
        table.add_column("Device", style="blue")
        table.add_column("Interface", style="magenta")
        table.add_column("Oper Status Threshold", style="green")
        table.add_column("Oper Status", style="red")
        table.add_column("Passed/Failed", style="yellow")
        for self.intf,value in self.parsed_interfaces.info.items():
            if 'oper_status' in value:
                counter = value['oper_status']
                if counter != oper_status_threshold:
                    table.add_row(self.device.alias,self.intf,str(oper_status_threshold),str(counter),'FAILED',style='red')
                    self.failed_interfaces = "failed"
                    self.enable_interface()
                else:
                    table.add_row(self.device.alias,self.intf,str(oper_status_threshold),str(counter),'PASSED',style='green')
        
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table)

        log.info(capture.get())

        # Should we pass or faile the test?
        if self.failed_interfaces:
            if not hasattr(self,'retry_count'):
                self.retry_count = 0
            
            self.retry_count += 1

            if self.retry_count < MAX_RETRIES:
                self.test_interface_oper_status()
            else:
                self.failed("Some interfaces are not operational after maximum retries")
        else:
            self.passed("All interfaces are operational")

    def enable_interface(self):
        self.device.configure(f'''interface { self.intf }
                              no shutdown
                              ''')
        time.sleep(20)
        self.capture_interface_state()

    @aetest.test
    def test_interface_description_matches_intent(self):
        self.failed_interfaces = {}
        table = Table(title="Interface Description Matches Intent")
        table.add_column("Device", style="blue")
        table.add_column("Interface", style="magenta")
        table.add_column("Intended Description", style="green")
        table.add_column("Actual Description", style="red")
        table.add_column("Passed/Failed", style="yellow")

        for self.intf, value in self.parsed_interfaces.info.items():
            actual_desc = value.get('description', None)
            for interface, intent_value in self.device.custom.interfaces.items():
                if self.intf == interface:
                    self.intended_desc = intent_value['description']
                    if actual_desc != self.intended_desc:
                        table.add_row(self.device.alias,self.intf,self.intended_desc,actual_desc,'FAILED',style='red')
                        self.failed_interfaces[self.intf] = self.intended_desc
                        self.update_interface_description()
                    else:
                        table.add_row(self.device.alias,self.intf,self.intended_desc,actual_desc,'PASSED',style='green')
        
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table)

        log.info(capture.get())

        # Should we pass or faile the test?
        if self.failed_interfaces:
            for self.intf, value in self.parsed_interfaces.info.items():
                actual_desc = value.get('description', None)
                for interface, intent_value in self.device.custom.interfaces.items():
                    if self.intf == interface:
                        self.intended_desc = intent_value['description']
                        if actual_desc != self.intended_desc:
                            table.add_row(self.device.alias,self.intf,self.intended_desc,actual_desc,'FAILED',style='red')
                            self.failed_interfacesp[self.intf] = self.intended_desc
                        else:
                            table.add_row(self.device.alias,self.intf,self.intended_desc,actual_desc,'PASSED',style='green')

            console = Console(record=True)
            with console.capture() as capture:
                console.print(table)
            
            log.info(capture.get())                    

            self.failed("We had to update the descriptions")
        else:
            self.passed("All descriptions matched intent")

    def update_interface_description(self):
        self.device.configure(f'''interface { self.intf }
                              description { self.intended_desc }
                              ''')
        self.capture_interface_state()

class common_cleanup(aetest.CommonCleanup):
    """Common Cleanup Section"""
    @aetest.subsection
    def disconnect_from_devices(self,testbed):
        testbed.disconnect()


