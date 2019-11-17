namespace motorController
{
    partial class Form1
    {
        /// <summary>
        /// Wymagana zmienna projektanta.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Wyczyść wszystkie używane zasoby.
        /// </summary>
        /// <param name="disposing">prawda, jeżeli zarządzane zasoby powinny zostać zlikwidowane; Fałsz w przeciwnym wypadku.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Kod generowany przez Projektanta formularzy systemu Windows

        /// <summary>
        /// Metoda wymagana do obsługi projektanta — nie należy modyfikować
        /// jej zawartości w edytorze kodu.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.serialPort1 = new System.IO.Ports.SerialPort(this.components);
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.cmbPort = new System.Windows.Forms.ComboBox();
            this.btnConnect = new System.Windows.Forms.Button();
            this.btnDisconnect = new System.Windows.Forms.Button();
            this.numBaud = new System.Windows.Forms.NumericUpDown();
            this.scrL = new System.Windows.Forms.TrackBar();
            this.scrR = new System.Windows.Forms.TrackBar();
            this.numL = new System.Windows.Forms.NumericUpDown();
            this.numR = new System.Windows.Forms.NumericUpDown();
            this.groupBox1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numBaud)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.scrL)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.scrR)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numL)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numR)).BeginInit();
            this.SuspendLayout();
            // 
            // serialPort1
            // 
            this.serialPort1.BaudRate = 57600;
            // 
            // groupBox1
            // 
            this.groupBox1.BackColor = System.Drawing.SystemColors.ScrollBar;
            this.groupBox1.Controls.Add(this.numBaud);
            this.groupBox1.Controls.Add(this.btnDisconnect);
            this.groupBox1.Controls.Add(this.cmbPort);
            this.groupBox1.Controls.Add(this.btnConnect);
            this.groupBox1.Location = new System.Drawing.Point(12, 12);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(167, 73);
            this.groupBox1.TabIndex = 0;
            this.groupBox1.TabStop = false;
            // 
            // cmbPort
            // 
            this.cmbPort.FormattingEnabled = true;
            this.cmbPort.Location = new System.Drawing.Point(6, 19);
            this.cmbPort.Name = "cmbPort";
            this.cmbPort.Size = new System.Drawing.Size(74, 21);
            this.cmbPort.TabIndex = 1;
            // 
            // btnConnect
            // 
            this.btnConnect.Location = new System.Drawing.Point(86, 17);
            this.btnConnect.Name = "btnConnect";
            this.btnConnect.Size = new System.Drawing.Size(75, 23);
            this.btnConnect.TabIndex = 2;
            this.btnConnect.Text = "Connect";
            this.btnConnect.UseVisualStyleBackColor = true;
            this.btnConnect.Click += new System.EventHandler(this.btnConnect_Click);
            // 
            // btnDisconnect
            // 
            this.btnDisconnect.Location = new System.Drawing.Point(86, 43);
            this.btnDisconnect.Name = "btnDisconnect";
            this.btnDisconnect.Size = new System.Drawing.Size(75, 23);
            this.btnDisconnect.TabIndex = 3;
            this.btnDisconnect.Text = "Disconnect";
            this.btnDisconnect.UseVisualStyleBackColor = true;
            this.btnDisconnect.Click += new System.EventHandler(this.btnDisconnect_Click);
            // 
            // numBaud
            // 
            this.numBaud.Increment = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.numBaud.Location = new System.Drawing.Point(6, 46);
            this.numBaud.Maximum = new decimal(new int[] {
            1000000,
            0,
            0,
            0});
            this.numBaud.Name = "numBaud";
            this.numBaud.Size = new System.Drawing.Size(74, 20);
            this.numBaud.TabIndex = 4;
            this.numBaud.Value = new decimal(new int[] {
            57600,
            0,
            0,
            0});
            this.numBaud.ValueChanged += new System.EventHandler(this.numBaud_ValueChanged);
            // 
            // scrL
            // 
            this.scrL.Location = new System.Drawing.Point(30, 91);
            this.scrL.Maximum = 255;
            this.scrL.Name = "scrL";
            this.scrL.Orientation = System.Windows.Forms.Orientation.Vertical;
            this.scrL.Size = new System.Drawing.Size(45, 171);
            this.scrL.TabIndex = 1;
            this.scrL.Scroll += new System.EventHandler(this.scrL_Scroll);
            // 
            // scrR
            // 
            this.scrR.Location = new System.Drawing.Point(111, 91);
            this.scrR.Maximum = 255;
            this.scrR.Name = "scrR";
            this.scrR.Orientation = System.Windows.Forms.Orientation.Vertical;
            this.scrR.Size = new System.Drawing.Size(45, 171);
            this.scrR.TabIndex = 2;
            this.scrR.Scroll += new System.EventHandler(this.scrR_Scroll);
            // 
            // numL
            // 
            this.numL.Location = new System.Drawing.Point(17, 257);
            this.numL.Maximum = new decimal(new int[] {
            255,
            0,
            0,
            0});
            this.numL.Name = "numL";
            this.numL.Size = new System.Drawing.Size(58, 20);
            this.numL.TabIndex = 3;
            this.numL.ValueChanged += new System.EventHandler(this.numL_ValueChanged);
            // 
            // numR
            // 
            this.numR.Location = new System.Drawing.Point(98, 257);
            this.numR.Maximum = new decimal(new int[] {
            255,
            0,
            0,
            0});
            this.numR.Name = "numR";
            this.numR.Size = new System.Drawing.Size(58, 20);
            this.numR.TabIndex = 4;
            this.numR.ValueChanged += new System.EventHandler(this.numR_ValueChanged);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(187, 289);
            this.Controls.Add(this.numR);
            this.Controls.Add(this.numL);
            this.Controls.Add(this.scrR);
            this.Controls.Add(this.scrL);
            this.Controls.Add(this.groupBox1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.groupBox1.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.numBaud)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.scrL)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.scrR)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numL)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numR)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.IO.Ports.SerialPort serialPort1;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.ComboBox cmbPort;
        private System.Windows.Forms.Button btnConnect;
        private System.Windows.Forms.Button btnDisconnect;
        private System.Windows.Forms.NumericUpDown numBaud;
        private System.Windows.Forms.TrackBar scrL;
        private System.Windows.Forms.TrackBar scrR;
        private System.Windows.Forms.NumericUpDown numL;
        private System.Windows.Forms.NumericUpDown numR;
    }
}

