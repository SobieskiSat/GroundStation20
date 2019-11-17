using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO.Ports;

namespace motorController
{
    public partial class Form1 : Form
    {
        bool scrLocked = false;
        bool numLocked = false;

        public void SendValues()
        {
            char charL = ASCIIEncoding.ASCII.GetChars(new[] { Convert.ToByte(scrL.Value) })[0];
            char charR = ASCIIEncoding.ASCII.GetChars(new[] { Convert.ToByte(scrR.Value) })[0];
            String msg = "";
            msg += charL;
            msg += charR;
            msg += '\n';
            System.Diagnostics.Debug.Write(msg);
            if (serialPort1.IsOpen)
            {
                serialPort1.Write(Convert.ToString(msg));
            }
        }

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            foreach (String portName in SerialPort.GetPortNames())
            {
                cmbPort.Items.Add(portName);
            }
            serialPort1.ReadTimeout = 2000;
            btnConnect.Enabled = true;
            btnDisconnect.Enabled = false;
        }

        private void numBaud_ValueChanged(object sender, EventArgs e)
        {
            serialPort1.BaudRate = Convert.ToInt32(numBaud.Value);
        }

        private void btnConnect_Click(object sender, EventArgs e)
        {
            serialPort1.PortName = cmbPort.SelectedItem.ToString();

            if (!serialPort1.IsOpen)
            {
                serialPort1.Open();
                btnConnect.Enabled = false;
                btnDisconnect.Enabled = true;
            }
        }

        private void btnDisconnect_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                serialPort1.Close();

                cmbPort.Items.Clear();
                foreach (String portName in SerialPort.GetPortNames())
                {
                    cmbPort.Items.Add(portName);
                }
                btnConnect.Enabled = true;
                btnDisconnect.Enabled = false;
            }
        }

        private void scrL_Scroll(object sender, EventArgs e)
        {
            if (!scrLocked)
            {
                numLocked = true;
                numL.Value = scrL.Value;
                numLocked = false;
                SendValues();
            }
        }
        private void numL_ValueChanged(object sender, EventArgs e)
        {
            if (!numLocked)
            {
                scrLocked = true;
                scrL.Value = Convert.ToInt32(numL.Value);
                scrLocked = false;
                SendValues();
            }
        }

        private void scrR_Scroll(object sender, EventArgs e)
        {
            if (!scrLocked)
            {
                numLocked = true;
                numR.Value = scrR.Value;
                numLocked = false;
                SendValues();
            }
        }
        private void numR_ValueChanged(object sender, EventArgs e)
        {

            if (!numLocked)
            {
                scrLocked = true;
                scrR.Value = Convert.ToInt32(numR.Value);
                scrLocked = false;
                SendValues();
            }
        }
    }
}
