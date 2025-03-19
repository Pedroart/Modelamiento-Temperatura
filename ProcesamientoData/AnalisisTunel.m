% Extraer la tabla de análisis
TunelAnalisis = A3P.tunel_3;



% Graficar los datos filtrados
figure;
plot(TunelAnalisis.IndiceTiempo, TunelAnalisis.TemperaturaAmbiente, 'LineWidth', 1.5);
hold on;
plot(TunelAnalisis.IndiceTiempo, TunelAnalisis.TemperaturaRetorno, 'LineWidth', 1.5);
plot(TunelAnalisis.IndiceTiempo, TunelAnalisis.EstadoValvula, 'LineWidth', 1.5);

% Configurar leyenda y etiquetas
legend({'TemperaturaAmbiente', 'TemperaturaRetorno', 'SensorZona1'}, 'Location', 'Best');
xlabel('Índice de Tiempo');
ylabel('Temperatura (°C)');
title('Análisis de Temperaturas con Filtro de Media Móvil');
grid on;
hold off;

%% Filtrado Señal

% Extraer la tabla de análisis
TunelAnalisis = Agrolatina.tunel_2;

% Obtener la derivada de la señal (diferencias finitas)
dT = diff(TunelAnalisis.TemperaturaAmbiente); 

% Limitar la derivada en el rango [-1,1]
dT_limited = max(min(dT, 0.2), -0.2);

% Integrar la derivada limitada usando suma acumulativa
reconstructed_signal = cumtrapz([TunelAnalisis.TemperaturaAmbiente(1); dT_limited]); 

% Graficar comparación de la señal original y reconstruida
figure;
plot(TunelAnalisis.IndiceTiempo, TunelAnalisis.TemperaturaAmbiente, 'b', 'LineWidth', 1.5);
hold on;
plot(TunelAnalisis.IndiceTiempo, reconstructed_signal, 'r--', 'LineWidth', 1.5);
legend({'Señal Original', 'Señal Reconstruida'}, 'Location', 'Best');
xlabel('Índice de Tiempo');
ylabel('Temperatura (°C)');
title('Reconstrucción de Señal a partir de Derivada Limitada');
grid on;
hold off;

%%

% Extraer la tabla de análisis
TunelAnalisis = Agrolatina.tunel_2;

% Obtener la derivada de la señal (diferencias finitas)
dT = diff(TunelAnalisis.TemperaturaAmbiente);

% Limitar la derivada en el rango [-1,1]
dT_limited = max(min(dT, 0.2), -0.2);

% Integrar la derivada limitada usando suma acumulativa
reconstructed_signal = cumtrapz([TunelAnalisis.TemperaturaAmbiente(1); dT_limited]); 

% Calcular el desplazamiento promedio entre señales
bias = mean(TunelAnalisis.TemperaturaAmbiente - reconstructed_signal);

% Ajustar la señal reconstruida sumando el sesgo
reconstructed_signal = reconstructed_signal + bias;

% Graficar comparación de la señal original y reconstruida ajustada
figure;
plot(TunelAnalisis.IndiceTiempo, TunelAnalisis.TemperaturaAmbiente, 'b', 'LineWidth', 1.5);
hold on;
plot(TunelAnalisis.IndiceTiempo, reconstructed_signal, 'r--', 'LineWidth', 1.5);
legend({'Señal Original', 'Señal Reconstruida Ajustada'}, 'Location', 'Best');
xlabel('Índice de Tiempo');
ylabel('Temperatura (°C)');
title('Reconstrucción de Señal con Derivada Limitada y Ajuste de Nivel');
grid on;
hold off;

%%

fc = 1;   % Frecuencia de corte en Hz
fs = 300;  % Frecuencia de muestreo en Hz

filteredSignal = lowpass(TunelAnalisis.TemperaturaAmbiente, fc, fs);

figure;
plot(TunelAnalisis.IndiceTiempo, TunelAnalisis.TemperaturaAmbiente, 'b', 'LineWidth', 1);
hold on;
plot(TunelAnalisis.IndiceTiempo, filteredSignal, 'r', 'LineWidth', 1.5);
legend({'Señal Original', 'Señal Filtrada'}, 'Location', 'Best');
xlabel('Tiempo');
ylabel('Amplitud');
title('Filtro Pasa Bajos con lowpass()');
grid on;


%%

% Extraer la señal y parámetros
y = TunelAnalisis.TemperaturaAmbiente;
fs = 50; % Frecuencia de muestreo (ajústala según tus datos)
N = length(y); % Número de muestras
t = TunelAnalisis.IndiceTiempo; % Tiempo de la señal

% Aplicar Transformada de Fourier
Y = fft(y); % FFT de la señal
f = (0:N-1)*(fs/N); % Eje de frecuencia

% Magnitud del espectro (solo la mitad por simetría)
P2 = abs(Y/N); % Normalizar
P1 = P2(1:N/2+1); % Tomar solo la mitad de los datos
f1 = f(1:N/2+1); % Frecuencia positiva

% Graficar espectro de frecuencia
figure;
plot(f1, P1, 'b', 'LineWidth', 1.5);
xlabel('Frecuencia (Hz)');
ylabel('Amplitud');
title('Espectro de Frecuencia de la Señal');
grid on;
xlim([0 fs/2]); % Limitar a la mitad de la frecuencia de muestreo
