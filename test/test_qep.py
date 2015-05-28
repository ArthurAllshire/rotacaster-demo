"""Unit tests for the Qep submodule"""

import unittest
from qep import Qep
import tempfile, os


class QepTest(unittest.TestCase):
    
    def setUp(self):
        tmpdir = tempfile.mkdtemp()
        # Create a temporary node tree
        self.QEP99 = "/sys/devices/ocp.2/00000000.epwmss/00000099.eqep"
        self.QEP99_dir = tmpdir + "/sys/devices/ocp.2/00000000.epwmss/00000099.eqep"
        Qep.IDS["QEP99"] = self.QEP99
        if not os.path.exists(self.PWM99A_dir):
            os.makedirs(self.PWM99A_dir)
    
    def set_qep_count(self, position):
        # Open the mode attribute file
        position_file = open(self.QEP99 + Qep.POSITION, "w")
        
        # Write the desired position into the file
        position_file.write(str(position))
        position_file.close()
        
    def read_file(self, path):
        file = open(path, "r")
        data = file.read()
        file.close()
        return data
        
    def test_qep_init(self):
        # Test default values
        q = Qep("QEP99")
        # Ensure that the qep's *ID* is being set
        self.assertEqual(q.qep_id, "QEP99")
        # Ensure that qep is correctly turning the id into a file
        self.assertEqual(q.qep_dir, self.QEP99)
        # Ensure that the encoder is in relative mode, as commanded
        self.assertEqual(Qep.MODE_RELATIVE, int(open(self.QEP99_dir+Qep.MODE).read()))
        # Ensure that we are zeroing the encoder file value
        self.assertEqual(0.0, float(open(self.QEP99_dir+Qep.POSITION).read()))
        
        # Test non default values
        #          ID        Counting Mode    Counts per Rev.   Period   Position
        q = Qep("QEP99", Qep.MODE_ABSOLUTE,     360,           100000000,   720)
        # Ensure that we are setting the right mode
        self.assertEqual(Qep.MODE_ABSOLUTE, int(open(self.QEP99_dir+Qep.MODE).read()))
        # Ensure that we are setting the correct counts per rev
        self.assertEqual(360, q.cpr)
        # Ensure that we are setting the period
        self.assertEqual(100000000, float(open(self.QEP99_dir+Qep.PERIOD).read()))
        # Ensure that we are setting the position
        self.assertEqual(720, float(open(self.QEP99_dir+Qep.POSITION).read()))
        
    def test_qep_file_output(self):
        pass