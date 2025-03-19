%% Import data from text file

%% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 18, "Encoding", "UTF-8");

% Specify range and delimiter
opts.DataLines = [2, Inf];
opts.Delimiter = ";";

% Especificar nombres de columnas y tipos de datos
opts.VariableNames = ["FechaHora", "TemperaturaAmbiente", "Caudal", "PresionPall", ...
                      "TemperaturaRetorno", "SensorZona1", "SensorZona2", "SensorZona3", ...
                      "SensorZona4", "SensorZona5", "SensorZona6", "SensorZona7", ...
                      "SensorZona8", "SensorZona9", "SensorZona10", "SensorZona11", ...
                      "SensorZona12", "Ventilacion"];
opts.VariableTypes = ["datetime", "double", "double", "double", "double", "double", "double", ...
                      "double", "double", "double", "double", "double", "double", "double", ...
                      "double", "double", "double", "double"];

% Especificar propiedades a nivel de archivo
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Especificar propiedades de las variables
opts = setvaropts(opts, "FechaHora", "InputFormat", "dd/MM/yyyy HH:mm:ss");

% Variables que deben procesarse como numéricas y sin caracteres no numéricos
varsToClean = ["TemperaturaAmbiente", "PresionPall", "TemperaturaRetorno", ...
               "SensorZona1", "SensorZona2", "SensorZona3", "SensorZona4", ...
               "SensorZona5", "SensorZona6", "SensorZona7", "SensorZona8", ...
               "SensorZona9", "SensorZona10", "SensorZona11", "SensorZona12"];

opts = setvaropts(opts, varsToClean, "TrimNonNumeric", true);
opts = setvaropts(opts, varsToClean, "ThousandsSeparator", ",");

% Import the data

% Especificar la carpeta donde están los archivos CSV
folderPath = "C:\Users\pedro\Documents\proyectos\Modelamiento-Temperatura\ProcesamientoData\pdc\";

% Obtener la lista de archivos CSV en la carpeta
csvFiles = dir(fullfile(folderPath, "*.csv"));

% Crear una estructura para almacenar las tablas
dataTables = struct();

% Leer cada archivo y almacenarlo en la estructura
for i = 1:length(csvFiles)
    % Obtener el nombre completo del archivo
    fileName = csvFiles(i).name;
    fullFilePath = fullfile(folderPath, fileName);

    % Crear un nombre de variable válido (sin espacios ni caracteres inválidos)
    %varName = matlab.lang.makeValidName(erase(fileName, ".csv"));
    varName = sprintf("tunel_%d", i)
    
    % Leer el archivo CSV en una tabla
    tbl = readtable(fullFilePath, opts);
    
    % Rellenar los valores NaN con el valor más cercano (Interpolación)
    for col = 2:width(tbl) % Saltar la primera columna (FechaHora)
        tbl{:, col} = fillmissing(tbl{:, col}, 'nearest')/10;
    end
    
    % Guardar la tabla en la estructura
    dataTables.(varName) = tbl;

    % Mostrar mensaje de progreso
    fprintf("Archivo leído: %s\n", fileName);
end

% Mostrar el contenido de la estructura con las tablas cargadas
disp(dataTables);

APDC = dataTables;

%% Clear temporary variables
clear opts
clear varNames
clear fileName
clear folderPath
clear fullFilePath
clear i
clear tbl
clear varName
clear col
clear dataTables
clear csvFiles
clear varsToClean
clear opts
clear varsToClean