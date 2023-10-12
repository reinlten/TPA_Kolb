s = tf("s");

%Variablen
R01 = 1*10^12;
R02 = 1*10^5;
C0 = 2*(10^-12);
C0ideal = 0;
Rs = 56000;
Rdut = 56000;

%Frequenzgang des Systems mit OPV
sys1 = (Rs*R01)/(Rs*R01 + Rdut*(Rs + R01 + s*Rs*R01*C0));

%Frequenzgang des Systems ohne OPV
sys2 = (Rs*R02)/(Rs*R02 + Rdut*(Rs + R02 + s*Rs*R02*C0));

%Idealder Frequenzgang
sysIdeal = (Rs*R01)/(Rs*R01 + Rdut*(Rs + R01 + s*Rs*R01*C0ideal));

%Optionen für die Diagramme
p1 = bodeoptions('cstprefs');
p1.FreqUnits = 'Hz';
p1.MagUnits = 'abs';
p1.MagScale = 'linear';
p1.YLimMode = 'manual';
p1.YLim(1) = {[0.3, 0.6]};
p1.YLim(2) = {[-90, 90]};
p1.Grid = 'off';
p1.Title.String = "";

%Plotten des ersten Diagramms
f1 = figure();
bodeplot(sys1, sysIdeal, ': r', p1, {1*2*pi, 1000000*2*pi});

%Formattierung der Achenbeschriftungen
ax = findall(f1,'Type','axes');
ax(1).XLabel.String = 'Frequenz / Hz';
ax(1).FontName = "Arial";
ax(1).FontSize = 10;
ax(2).YLabel.String = 'φ / °';
ax(2).FontName = "Arial";
ax(2).FontSize = 10;
ax(3).YLabel.String = 'Û2 / Û0 / -';
ax(3).FontName = "Arial";
ax(3).FontSize = 10;
legend("Frequenzgang mit OPV", "Idealer Frequenzgang");

%Plotten des zweiten Diagramms
f2 = figure();
bodeplot(sys2, sysIdeal, ': r', p1, {1*2*pi, 1000000*2*pi});

%Formattierung der Achenbeschriftungen
ax = findall(f2,'Type','axes');
ax(1).XLabel.String = 'Frequenz / Hz';
ax(1).FontName = "Arial";
ax(1).FontSize = 10;
ax(2).YLabel.String = 'φ / °';
ax(2).FontName = "Arial";
ax(2).FontSize = 10;
ax(3).YLabel.String = 'Û2 / Û0 / -';
ax(3).FontName = "Arial";
ax(3).FontSize = 10;
legend("Frequenzgang ohne OPV", "Idealer Frequenzgang");