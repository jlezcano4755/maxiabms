#!/bin/bash

# Configurando gráficos de grafana a Maxia BMS
cd /usr/share/grafana/public/views
sed -i 's/"#F05A28"/"#af297a"/g' index*.html
sed -i 's/"#F05A28"/"#af297a"/g' error*.html
sed -i 's/"Loading Grafana"/"Cargando Maxia BMS..."/g' index*.html

# Antes de esto crea un Backup de los archivos de la aplicación que se editarán por si algo falla
cp -r /usr/share/grafana/public/build/ /usr/share/grafana/public/backup/
cd /usr/share/grafana/public/build

# TimePicker
sed -i 's/"Last 5 minutes"/"Últimos 5 minutos"/g' app*.js*
sed -i 's/"Last 15 minutes"/"Últimos 15 minutos"/g' app*.js*
sed -i 's/"Last 30 minutes"/"Últimos 30 minutos"/g' app*.js*
sed -i 's/"Last 1 hour"/"Última hora"/g' app*.js*
sed -i 's/"Last 3 hours"/"Últimas 3 horas"/g' app*.js*
sed -i 's/"Last 6 hours"/"Últimas 6 horas"/g' app*.js*
sed -i 's/"Last 12 hours"/"Últimas 12 horas"/g' app*.js*
sed -i 's/"Last 24 hours"/"Últimas 24 horas"/g' app*.js*
sed -i 's/"Last 2 days"/"Últimos 2 días"/g' app*.js*
sed -i 's/"Last 7 days"/"Últimos 7 días"/g' app*.js*
sed -i 's/"Last 30 days"/"Últimos 30 días"/g' app*.js*
sed -i 's/"Last 90 days"/"Últimos 90 días"/g' app*.js*
sed -i 's/"Last 6 months"/"Últimos 6 meses"/g' app*.js*
sed -i 's/"Last 1 year"/"Último año"/g' app*.js*
sed -i 's/"Last 2 years"/"Últimos 2 años"/g' app*.js*
sed -i 's/"Last 5 years"/"Últimos 5 años"/g' app*.js*
sed -i 's/"Yesterday"/"Ayer"/g' app*.js*
sed -i 's/"Day before yesterday"/"Antes de ayer"/g' app*.js*
sed -i 's/"This day last week"/"Este día de la semana pasada"/g' app*.js*
sed -i 's/"Previous week"/"Semana anterior"/g' app*.js*
sed -i 's/"Previous month"/"Mes anterior"/g' app*.js*
sed -i 's/"Previous year"/"Año anterior"/g' app*.js*
sed -i 's/"Today"/"Hoy"/g' app*.js*
sed -i 's/"Today so far"/"Hoy hasta ahora"/g' app*.js*
sed -i 's/"This week"/"Esta semana"/g' app*.js*
sed -i 's/"This week so far"/"Esta semana hasta ahora"/g' app*.js*
sed -i 's/"This month"/"Este mes"/g' app*.js*
sed -i 's/"This month so far"/"Este mes hasta ahora"/g' app*.js*
sed -i 's/"This year"/"Este año"/g' app*.js*
sed -i 's/"This year so far"/"Este año hasta ahora"/g' app*.js*
sed -i 's/"Next 30 minutes"/"Próximos 30 minutos"/g' app*.js*

sed -i 's/"Russian Federation"/"Federación Rusa"/g' app*.js*

sed -i 's/"It looks like you haven'\''t used this timer picker before. As soon as you enter some time intervals, recently used intervals will appear here."/"Parece que no has usado este selector de tiempo antes. Tan pronto como introduzca algunos intervalos de tiempo, los intervalos utilizados recientemente aparecerán aquí."/g' app*.js*
sed -i 's/"Read the documentation"/"Lea la documentación"/g' app*.js*
sed -i 's/" to find out more about how to enter custom time ranges."/"para saber más sobre cómo introducir rangos de tiempo personalizados."/g' app*.js*

sed -i 's/title:"Recently used absolute ranges"/title:"Rangos absolutos utilizados recientemente"/g' app*.js*
sed -i 's/title:"Relative time ranges"/title:"Rangos de tiempo relativos"/g' app*.js*
sed -i 's/(d,null,"Absolute time range")/(d,null,"Rango de tiempo absoluto")/g' app*.js*
sed -i 's/"Apply time range"/"Aplicar el rango de tiempo"/g' app*.js*
sed -i 's/"Browser Time"/"Tiempo de navegación"/g' app*.js*
sed -i 's/"Change time zone"/"Cambiar la zona horaria"/g' app*.js*
sed -i 's/"Other quick ranges"/"Otros rangos rápidos"/g' app*.js*
sed -i 's/"From"/"Desde"/g' app*.js*
sed -i 's/"To"/"A"/g' app*.js*

sed -i 's/"Local browser time"/"Hora del navegador local"/g' app*.js*
sed -i 's/{className:"text-center"},"to")/{className:"text-center"},"a")/g' app*.js*

# Login page
sed -i 's/"Grafana"/"Maxia BMS"/g' app*.js*
sed -i 's/"Welcome to Grafana"/"Bienvenido a Maxia BMS"/g' app*.js*
sed -i 's/"Don'\''t get in the way of the data"/"No se interponga en el camino de los datos | Desarrollado por Maxia BMS"/g' app*.js*
sed -i 's/"Your single pane of glass"/"Su único cristal | Desarrollado por Maxia BMS"/g' app*.js*
sed -i 's/"Built better together"/"Construir mejor juntos | Desarrollado por Maxia BMS"/g' app*.js*
sed -i 's/"Democratising data"/"Democratizar los datos | Desarrollado por Maxia BMS"/g' app*.js*

sed -i 's/"Email or username"/"Email o usuario"/g' app*.js*
sed -i 's/"Password"/"Clave"/g' app*.js*
sed -i 's/"Forgot your password?"/"¿Ha olvidado su contraseña?"/g' app*.js*
sed -i 's/"Log in"/"Acceder"/g' app*.js*
sed -i 's/"Logged in"/"Conectado"/g' app*.js*
sed -i 's/placeholder="email or username"/placeholder="email o usuario"/g' app*.js*
sed -i 's/placeholder="password"/placeholder="clave"/g' app*.js*
sed -i 's/"Logging in..."/"Ingresando..."/g' app*.js*
sed -i 's/"Email or username is required"/"El email o usuario es obligatorio"/g' app*.js*
sed -i 's/"Password is required"/"La clave es obligatoria"/g' app*.js*

# Otros (por clasificar)
sed -i 's/title:"Dashboards"/title:"Dashboards"/g' app*.js*
sed -i 's/tooltip:"Save dashboard"/tooltip:"Guardar dashboard"/g' app*.js*
sed -i 's/tooltip:"Dashboard settings"/tooltip:"Configuraciones de dashboard"/g' app*.js*
sed -i 's/tooltip:"Add panel"/tooltip:"Agregar panel"/g' app*.js*
sed -i 's/tooltip:"Cycle view mode"/tooltip:"Modo de vista del ciclo"/g' app*.js*
sed -i 's/"Time range zoom out "/"Time range zoom out "/g' app*.js*
sed -i 's/"Mark as favorite"/"Marcar como favorito"/g' app*.js*
sed -i 's/"Share dashboard"/"Compartir dashboard"/g' app*.js*
sed -i 's/label:"Save current variable values as dashboard default"/label:"Guardar los valores actuales de las variables como valores por defecto del dashboard"/g' app*.js*
sed -i 's/label:"Save current time range as dashboard default"/label:"Guardar el intervalo de tiempo actual como valor predeterminado del dashboard"/g' app*.js*
sed -i 's/placeholder:"Add a note to describe your changes..."/placeholder:"Añade una nota para describir tus cambios..."/g' app*.js*
sed -i 's/title:"Save dashboard"/title:"Guardar dashboard"/g' app*.js*
sed -i 's/"Save"/"Guardar"/g' app*.js*
sed -i 's/"Cancel"/"Cancelar"/g' app*.js*
sed -i 's/" ago"/"  hace"/g' app*.js*
sed -i 's/"Press ESC to exit Kiosk mode"/"Pulse ESC para salir del modo Kiosco"/g' app*.js*
sed -i 's/tooltip:"Refresh dashboard"/tooltip:"Refrescar dashboard"/g' app*.js*

sed -i 's/"Jan"/"Ene"/g' app*.js*
sed -i 's/"Feb"/"Feb"/g' app*.js*
sed -i 's/"Mar"/"Mar"/g' app*.js*
sed -i 's/"Apr"/"Abr"/g' app*.js*
sed -i 's/"May"/"May"/g' app*.js*
sed -i 's/"Jun"/"Jun"/g' app*.js*
sed -i 's/"Jul"/"Jul"/g' app*.js*
sed -i 's/"Aug"/"Ago"/g' app*.js*
sed -i 's/"Sep"/"Sep"/g' app*.js*
sed -i 's/"Oct"/"Oct"/g' app*.js*
sed -i 's/"Nov"/"Nov"/g' app*.js*
sed -i 's/"Dec"/"Dic"/g' app*.js*

sed -i 's/"Mon"/"Lun"/g' app*.js*
sed -i 's/"Tue"/"Mar"/g' app*.js*
sed -i 's/"Wed"/"Mier"/g' app*.js*
sed -i 's/"Thu"/"Jue"/g' app*.js*
sed -i 's/"Fri"/"Vier"/g' app*.js*
sed -i 's/"Sat"/"Sáb"/g' app*.js*
sed -i 's/"Sun"/"Dom"/g' app*.js*

sleep 5
echo "¡Cambios realizados! Borra la caché del navegador para ver los cambios. (CTRL+F5)"
