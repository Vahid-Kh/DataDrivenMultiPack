function [ErrCode,MotiveM,SuctionM,EntrainmentRatio] = EjectorRom...
    (EjectorName,MotiveP,MotiveT, MotiveH, SuctionP, SuctionSh, SuctionH, OutletP)
% Ejector Rom Model Usage:  
%  Units: P [Pa]. T [K]. Sh [K]. H [J/kg]. m [kg/s]. EntrainmentRatio = SuctionM/MotiveM [-]
%  
%  Inputs:
%   Possible ejector names:
%    EjectorName$ = 'Multi Ejector HP 1875'
%    EjectorName$ = 'Multi Ejector HP 3875'
%    EjectorName$ = 'Multi Ejector LP 935'
%    EjectorName$ = 'Multi Ejector LP 1935'
%    EjectorName$ = 'CTM 1 LE 200'
%    EjectorName$ = 'CTM 1 LE 400'
%    EjectorName$ = 'CTM 2 LE 600'
%
%   MotiveP, MotiveT,MotiveH: Motive pressure, temperature and enthalpy respectively
%   SuctionP,SuctionSh,SuctionH: Suction pressure, superheat and enthalpy respectively
%   OutletP: Outlet pressure 
%    
%  Possible values of ErrCode:
%    0  : No errors
%   -1  : Coolselector®2 installation not found
%   -2  : Requested ejector not found
%   If ErrCode is larger than 0 then operation is outside ejector envelope:
%     A value of 1 indicates outside suction envelope
%     A value of 10 indicates outside motive envelope
%     A value of 100 indicates outside pressure lift envelope     
%     These values are added so that e.g. ErrCode = 101 means outside suction and lift envelope (but inside motive envelope) 
%

if not(libisloaded('DFEjector'))
    loadlibrary('DFEjector')
end
[ErrCode,~,MotiveM,SuctionM,EntrainmentRatio] = calllib('DFEjector','EjectorPerformance',...
    EjectorName,MotiveP,MotiveT, MotiveH, SuctionP, SuctionSh, SuctionH, OutletP,...
    0,0,0);
end

