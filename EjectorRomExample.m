Inputs.EjectorName = 'Multi Ejector HP 3875';
Inputs.P_motive = 90e5;
Inputs.T_motive = 35+273.15;
Inputs.H_motive = 299034;
Inputs.P_suction = 28e5;
Inputs.DT_sh_suction = 8;
Inputs.H_suction = 446173.6;
Inputs.P_outlet = 38e5;
[ErrCode,Outputs.m_motive,Outputs.m_suction,Outputs.EntrainmentRatio] = EjectorRom(...
    Inputs.EjectorName,Inputs.P_motive,Inputs.T_motive,Inputs.H_motive,Inputs.P_suction,Inputs.DT_sh_suction,Inputs.H_suction,Inputs.P_outlet);

matlabroot