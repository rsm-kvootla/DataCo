#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pandas as pd
import numpy as np


# In[36]:


df = pd.read_csv('datanew2.csv')


# In[37]:


df['late'] = df['days_for_shipping_(real)'] > df['days_for_shipment_(scheduled)']

# Map regions to countries
region_to_countries = {'Central America': ['Belice', 'Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'México', 'Nicaragua', 'Panamá'], 'East of USA': ['Estados Unidos'], 'South America': ['Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Ecuador', 'Guayana Francesa', 'Guyana', 'Paraguay', 'Perú', 'Surinam', 'Uruguay', 'Venezuela'], 'South of  USA ': ['Estados Unidos'], 'West of USA ': ['Estados Unidos']}



# Map regions to cities
region_to_cities = {'Central America': ['Acayucan', 'Acuña', 'Acámbaro', 'Altotonga', 'Amatitlán', 'Antiguo Cuscatlán', 'Apatzingán de la Constitución', 'Apodaca', 'Apopa', 'Arraiján', 'Atlixco', 'Azcapotzalco', 'Cadereyta', 'Campeche', 'Cancún', 'Celaya', 'Chetumal', 'Chihuahua', 'Chilpancingo', 'Chimaltenango', 'Chinandega', 'Chinautla', 'Choloma', 'Cholula', 'Choluteca', 'Ciudad del Carmen', 'Coacalco', 'Coatzacoalcos', 'Colima', 'Colón', 'Coyoacán', 'Cuajimalpa', 'Cuautitlán', 'Cuernavaca', 'Culiacán', 'Cuscatancingo', 'Córdoba', 'David', 'Delgado', 'Delicias', 'Durango', 'El Progreso', 'Ensenada', 'Escuintla', 'Estelí', 'Fresnillo de González Echeverría', 'Frontera', 'Garza García', 'General Escobedo', 'Granada', 'Guadalajara', 'Guamúchil', 'Guanajuato', 'Guasave', 'Guatemala City', 'Guaymas', 'Guzmán', 'Gómez Palacio', 'Hermosillo', 'Heroica Zitácuaro', 'Hidalgo', 'Huehuetenango', 'Huixquilucan', 'Iguala', 'Ilopango', 'Irapuato', 'Ixtapaluca', 'Jiutepec', 'Juárez', 'La Ceiba', 'La Chorrera', 'La Paz', 'Lagos de Moreno', 'León', 'Linares', 'Los Mochis', 'Lázaro Cárdenas', 'Madero', 'Managua', 'Manzanillo', 'Masaya', 'Matagalpa', 'Matehuala', 'Mejicanos', 'Melchor Ocampo', 'Metepec', 'Mexicali', 'Mexico City', 'Miguel Hidalgo', 'Milpa Alta', 'Miramar', 'Mixco', 'Monclova', 'Monterrey', 'Morelia', 'Mérida', 'Nicolás Romero', 'Nicoya', 'Nuevo Laredo', 'Obregón', 'Ocotlán', 'Orizaba', 'Panama City', 'Petapa', 'Piedras Negras', 'Poza Rica de Hidalgo', 'Progreso', 'Puebla', 'Puerto Vallarta', 'Querétaro', 'Quetzaltenango', 'Reynosa', 'Rosarito', 'Río Bravo', 'Sahuayo de José María Morelos', 'Salamanca', 'Salina Cruz', 'Saltillo', 'San Andrés Tuxtla', 'San Cristóbal de Las Casas', 'San Francisco del Rincón', 'San Ignacio', 'San Juan del Río', 'San Luis Potosí', 'San Luis Río Colorado', 'San Martín', 'San Miguelito', 'San Pablo de las Salinas', 'San Pedro Sula', 'San Salvador', 'Santa Ana', 'Santa Catarina', 'Silao', 'Soledad Díez Gutiérrez', 'Sonsonate', 'Soyapango', 'Tampico', 'Tapachula', 'Tecomán', 'Tegucigalpa', 'Tehuacán', 'Temixco', 'Tepic', 'Teziutlán', 'Tijuana', 'Tipitapa', 'Tlalnepantla', 'Tlalpan', 'Tlaquepaque', 'Toluca', 'Torreón', 'Tulancingo', 'Tuxtla Gutiérrez', 'Valle Hermoso', 'Valles', 'Veracruz', 'Victoria', 'Villa Canales', 'Villa Frontera', 'Villa Nueva', 'Villahermosa', 'Zacatecas', 'Zapopan', 'Zihuatanejo'], 'East of USA': ['Akron', 'Allentown', 'Altoona', 'Andover', 'Atlantic City', 'Auburn', 'Baltimore', 'Bangor', 'Bayonne', 'Belleville', 'Bethlehem', 'Beverly', 'Bowling Green', 'Bridgeton', 'Bristol', 'Buffalo', 'Burlington', 'Cambridge', 'Chester', 'Cincinnati', 'Cleveland', 'Clifton', 'Clinton', 'Columbia', 'Columbus', 'Concord', 'Cranston', 'Cuyahoga Falls', 'Dover', 'Dublín', 'East Orange', 'Elyria', 'Everett', 'Fairfield', 'Franklin', 'Freeport', 'Gaithersburg', 'Grove City', 'Hackensack', 'Hamilton', 'Hempstead', 'Holyoke', 'Jamestown', 'Kent', 'Lakewood', 'Lancaster', 'Laurel', 'Lawrence', 'Leominster', 'Lewiston', 'Linden', 'Lindenhurst', 'Long Beach', 'Lorain', 'Lowell', 'Malden', 'Manchester', 'Marion', 'Marlborough', 'Mason', 'Medina', 'Mentor', 'Meriden', 'Middletown', 'Milford', 'Morristown', 'Mount Vernon', 'Nashua', 'New Bedford', 'New Brunswick', 'New Rochelle', 'New York City', 'Newark', 'Niagara Falls', 'Norwich', 'Oceanside', 'Orange', 'Parma', 'Passaic', 'Paterson', 'Perth Amboy', 'Philadelphia', 'Plainfield', 'Providence', 'Quincy', 'Reading', 'Revere', 'Rochester', 'Rockville', 'Rome', 'Shelton', 'Springfield', 'Toledo', 'Troy', 'Utica', 'Vineland', 'Warwick', 'Washington', 'Waterbury', 'Watertown', 'Westfield', 'Wheeling', 'Wilmington', 'Woonsocket', 'Yonkers', 'York'], 'South America': ['Abreu e Lima', 'Acarigua', 'Altamira', 'Americana', 'Ananindeua', 'Andradina', 'Antofagasta', 'Anápolis', 'Apartadó', 'Apucarana', 'Aracaju', 'Aracati', 'Araguaína', 'Arapiraca', 'Arapongas', 'Araranguá', 'Araraquara', 'Arauca', 'Araucária', 'Araçatuba', 'Arcoverde', 'Arequipa', 'Arica', 'Ariquemes', 'Armenia', 'Asunción', 'Avellaneda', 'Ayacucho', 'Açu', 'Bagé', 'Bahía Blanca', 'Balneário Camboriú', 'Barbacena', 'Barcelona', 'Barquisimeto', 'Barra Mansa', 'Barra do Piraí', 'Barranca', 'Barranquilla', 'Barreiras', 'Barreirinhas', 'Barretos', 'Barueri', 'Baruta', 'Bayeux', 'Bello', 'Belo Horizonte', 'Bento Gonçalves', 'Betim', 'Bezerros', 'Birigui', 'Blumenau', 'Boa Esperança', 'Boa Vista', 'Bogotá', 'Bolívar', 'Bom Jesus da Lapa', 'Bragança Paulista', 'Brasília', 'Brumado', 'Bucaramanga', 'Buenos Aires', 'Buriticupu', 'Cabimas', 'Cabo Frio', 'Cabo de Santo Agostinho', 'Cagua', 'Cajamarca', 'Cajazeiras', 'Calabozo', 'Calama', 'Callao', 'Camaragibe', 'Camaçari', 'Cambé', 'Camocim', 'Campina Grande', 'Campo Grande', 'Campo Limpo Paulista', 'Canoas', 'Caracas', 'Caraguatatuba', 'Carapicuíba', 'Carora', 'Cartagena', 'Cartago', 'Cassilândia', 'Castanhal', 'Catalão', 'Catanduva', 'Catia La Mar', 'Caucaia', 'Caxias do Sul', 'Cayenne', 'Caçador', 'Chapecó', 'Charallave', 'Chiclayo', 'Chillán', 'Chimbote', 'Chincha Alta', 'Cidade Ocidental', 'Cipolletti', 'Ciénaga', 'Coari', 'Cochabamba', 'Colombo', 'Comodoro Rivadavia', 'Concepción del Uruguay', 'Conselheiro Lafaiete', 'Contagem', 'Copiapó', 'Corrientes', 'Cotia', 'Crato', 'Criciúma', 'Cruz das Almas', 'Cruzeiro', 'Cruzeiro do Sul', 'Cubatão', 'Cuenca', 'Cuiabá', 'Cumaná', 'Curitiba', 'Córdoba', 'Cúa', 'Cúcuta', 'Diadema', 'Divinópolis', 'Dos Quebradas', 'Dourados', 'Duitama', 'Duque de Caxias', 'El Limón', 'El Tigre', 'Envigado', 'Erechim', 'Esquina', 'Eunápolis', 'Facatativá', 'Farroupilha', 'Feira de Santana', 'Fernando de la Mora', 'Florencia', 'Floriano', 'Floridablanca', 'Fortaleza', 'Franca', 'Francisco Beltrão', 'Francisco Morato', 'Franco da Rocha', 'Garanhuns', 'Gaspar', 'Girón', 'Goiânia', 'Grajaú', 'Gravataí', 'Gravatá', 'Guacara', 'Guanambi', 'Guanare', 'Guarapari', 'Guarapuava', 'Guaratinguetá', 'Guarenas', 'Guarujá', 'Guarulhos', 'Guatire', 'Guayana', 'Guayaquil', 'Gurupi', 'Huancayo', 'Huaraz', 'Ibagué', 'Ibirité', 'Ibiúna', 'Igarassu', 'Ijuí', 'Ilhéus', 'Ilo', 'Indaial', 'Indaiatuba', 'Ipatinga', 'Ipiales', 'Iquique', 'Iquitos', 'Itaituba', 'Itajaí', 'Itamaraju', 'Itapecerica da Serra', 'Itapecuru Mirim', 'Itapetininga', 'Itapeva', 'Itapevi', 'Itaúna', 'Itu', 'Ituiutaba', 'Jaboticabal', 'Jacareí', 'Jacobina', 'Jamundí', 'Jataí', 'Jaú', 'Jequié', 'Ji-Paraná', 'Joinville', 'José Bonifácio', 'João Pessoa', 'Juazeiro', 'Juiz de Fora', 'Juliaca', 'Jundiaí', 'Junín', 'Jurema', 'La Paz', 'La Pintana', 'La Plata', 'La Rioja', 'Lajeado', 'Lambaré', 'Las Piedras', 'Lençóis Paulista', 'Lima', 'Limeira', 'Limoeiro do Norte', 'Linden', 'Linhares', 'Lins', 'Londrina', 'Lorena', 'Los Patios', 'Los Ángeles', 'Macapá', 'Maceió', 'Malambo', 'Manacapuru', 'Manaus', 'Manizales', 'Mar del Plata', 'Maracaibo', 'Maracay', 'Maringá', 'Maturín', 'Mauá', 'Medellín', 'Mendoza', 'Mococa', 'Mogi das Cruzes', 'Montenegro', 'Montería', 'Montes Claros', 'Montevideo', 'Mosquera', 'Mossoró', 'Mérida', 'Natal', 'Navegantes', 'Neiva', 'Neuquén', 'Niterói', 'Nova Serrana', 'Novo Cruzeiro', 'Novo Gama', 'Ocaña', 'Oriximiná', 'Oruro', 'Osasco', 'Osorno', 'Paita', 'Palhoça', 'Palmares', 'Palmira', 'Palo Negro', 'Paracatu', 'Paramaribo', 'Paranaguá', 'Paraná', 'Parintins', 'Passo Fundo', 'Passos', 'Pasto', 'Pato Branco', 'Patrocínio', 'Paulista', 'Paysandú', 'Paço do Lumiar', 'Pelotas', 'Penedo', 'Pereira', 'Petare', 'Petrópolis', 'Piedecuesta', 'Pilar', 'Pindamonhangaba', 'Pinheiro', 'Pirapora', 'Pitalito', 'Piura', 'Ponte Nova', 'Pontes e Lacerda', 'Porlamar', 'Porto Alegre', 'Portoviejo', 'Posadas', 'Potosí', 'Pouso Alegre', 'Poços de Caldas', 'Praia Grande', 'Presidencia Roque Sáenz Peña', 'Presidente Dutra', 'Presidente Prudente', 'Pucallpa', 'Puente Alto', 'Puerto La Cruz', 'Puerto Montt', 'Puno', 'Punta Arenas', 'Quevedo', 'Quibdó', 'Quilmes', 'Quito', 'Quixadá', 'Rancagua', 'Recife', 'Registro', 'Resende', 'Resistencia', 'Ribeirão Preto', 'Riberalta', 'Rio Branco', 'Rio Grande', 'Rivera', 'Rolândia', 'Rondonópolis', 'Rosario', 'Sabanalarga', 'Salta', 'Salvador', 'San Antonio', 'San Bernardo', 'San Carlos del Zulia', 'San Cristóbal', 'San Fernando del Valle de Catamarca', 'San José de Guanipa', 'San Juan', 'San Justo', 'San Lorenzo', 'San Luis', 'San Nicolás de los Arroyos', 'San Rafael', 'San Salvador de Jujuy', 'Santa Cruz de la Sierra', 'Santa Cruz do Sul', 'Santa Fe', 'Santa Helena', 'Santa Marta', 'Santa Rosa', 'Santana de Parnaíba', 'Santarém', 'Santiago de Chile', 'Santiago del Estero', 'Santo André', 'Santo Domingo de los Colorados', 'Santos', 'Sapucaia do Sul', 'Senhor do Bonfim', 'Seropédica', 'Serra', 'Simões Filho', 'Sinop', 'Soacha', 'Sobral', 'Sogamoso', 'Soledad', 'Sorocaba', 'Sorriso', 'Sousa', 'Sucre', 'Sumaré', 'Surubim', 'São Benedito', 'São Bernardo do Campo', 'São Gonçalo', 'São José dos Campos', 'São Leopoldo', 'São Luís', 'São Miguel dos Campos', 'São Paulo', 'São Pedro da Aldeia', 'São Vicente', 'Taboão da Serra', 'Talara', 'Talcahuano', 'Tartagal', 'Tatuí', 'Taubaté', 'Teresina', 'Teresópolis', 'Tianguá', 'Tinaquillo', 'Toledo', 'Trinidad', 'Trujillo', 'Tupã', 'Turmero', 'Uberaba', 'Uberlândia', 'Umuarama', 'Uruguaiana', 'Vacaria', 'Valencia', 'Valinhos', 'Valle de La Pascua', 'Valledupar', 'Valparaíso', 'Valparaíso de Goiás', 'Vassouras', 'Vespasiano', 'Vilhena', 'Villa Alemana', 'Villavicencio', 'Vitória', 'Vitória da Conquista', 'Vitória de Santo Antão', 'Viña del Mar', 'Votuporanga', 'Várzea Grande', 'Yacuiba', 'Yaritagua', 'Yopal', 'Águas Lindas de Goiás'], 'South of  USA ': ['Alexandria', 'Apopka', 'Arlington', 'Asheville', 'Athens', 'Atlanta', 'Auburn', 'Boca Raton', 'Bossier City', 'Bowling Green', 'Boynton Beach', 'Bristol', 'Burlington', 'Cary', 'Charlotte', 'Charlottesville', 'Chattanooga', 'Chesapeake', 'Clarksville', 'Columbia', 'Columbus', 'Concord', 'Conway', 'Coral Springs', 'Daytona Beach', 'Decatur', 'Delray Beach', 'Deltona', 'Durham', 'East Point', 'Fayetteville', 'Florence', 'Fort Lauderdale', 'Franklin', 'Gastonia', 'Georgetown', 'Greensboro', 'Greenville', 'Gulfport', 'Hampton', 'Harrisonburg', 'Hattiesburg', 'Henderson', 'Hendersonville', 'Hialeah', 'Hickory', 'Hollywood', 'Homestead', 'Hoover', 'Hot Springs', 'Huntsville', 'Jackson', 'Jacksonville', 'Johnson City', 'Jonesboro', 'Jupiter', 'Kenner', 'Kissimmee', 'Knoxville', 'Lafayette', 'Lake Charles', 'Lakeland', 'Little Rock', 'Louisville', 'Líbano', 'Macon', 'Margate', 'Marietta', 'Memphis', 'Miami', 'Miramar', 'Mobile', 'Monroe', 'Montgomery', 'Mount Pleasant', 'Murfreesboro', 'Murray', 'Nashville', 'Newport News', 'North Charleston', 'North Miami', 'Orlando', 'Ormond Beach', 'Owensboro', 'Palm Coast', 'Pembroke Pines', 'Pensacola', 'Pine Bluff', 'Plantation', 'Pompano Beach', 'Port Saint Lucie', 'Raleigh', 'Richmond', 'Rock Hill', 'Roswell', 'Saint Petersburg', 'Salem', 'Sandy Springs', 'Sanford', 'Smyrna', 'Southaven', 'Springdale', 'Springfield', 'Suffolk', 'Summerville', 'Tallahassee', 'Tamarac', 'Tampa', 'Texarkana', 'Thomasville', 'Tuscaloosa', 'Virginia Beach', 'Warner Robins', 'Waynesboro', 'West Palm Beach', 'Wilmington', 'Wilson', 'Woodstock'], 'West of USA ': ['Albuquerque', 'Anaheim', 'Antioch', 'Apple Valley', 'Arvada', 'Auburn', 'Aurora', 'Avondale', 'Bakersfield', 'Bellevue', 'Bellingham', 'Billings', 'Boise', 'Bozeman', 'Brentwood', 'Broomfield', 'Bullhead City', 'Burbank', 'Caldwell', 'Camarillo', 'Carlsbad', 'Chandler', 'Chico', 'Chula Vista', 'Citrus Heights', 'Clovis', 'Coachella', 'Colorado Springs', 'Commerce City', 'Concord', 'Costa Mesa', 'Covington', 'Danville', 'Davis', 'Denver', 'Des Moines', 'Draper', 'Dublín', 'Edmonds', 'El Cajon', 'Encinitas', 'Englewood', 'Escondido', 'Eugene', 'Everett', 'Fairfield', 'Farmington', 'Fort Collins', 'Fresno', 'Gilbert', 'Glendale', 'Great Falls', 'Gresham', 'Helena', 'Henderson', 'Hesperia', 'Hillsboro', 'Huntington Beach', 'Inglewood', 'Kent', 'La Mesa', 'Laguna Niguel', 'Lake Elsinore', 'Lake Forest', 'Lakewood', 'Lancaster', 'Las Cruces', 'Las Vegas', 'Layton', 'Lehi', 'Lodi', 'Logan', 'Long Beach', 'Longmont', 'Longview', 'Los Angeles', 'Louisville', 'Loveland', 'Manteca', 'Marysville', 'Medford', 'Meridian', 'Mesa', 'Mission Viejo', 'Missoula', 'Modesto', 'Montebello', 'Moreno Valley', 'Morgan Hill', 'Murray', 'Murrieta', 'North Las Vegas', 'Oakland', 'Oceanside', 'Olympia', 'Ontario', 'Orem', 'Oxnard', 'Parker', 'Pasadena', 'Pasco', 'Peoria', 'Phoenix', 'Pico Rivera', 'Pleasant Grove', 'Pocatello', 'Pomona', 'Portland', 'Provo', 'Pueblo', 'Rancho Cucamonga', 'Redding', 'Redlands', 'Redmond', 'Redondo Beach', 'Redwood City', 'Reno', 'Renton', 'Rio Rancho', 'Riverside', 'Roseville', 'Sacramento', 'Salem', 'Salinas', 'Salt Lake City', 'San Bernardino', 'San Clemente', 'San Diego', 'San Francisco', 'San Gabriel', 'San Jose', 'San Luis Obispo', 'San Mateo', 'Santa Ana', 'Santa Barbara', 'Santa Clara', 'Santa Fe', 'Santa Maria', 'Scottsdale', 'Seattle', 'Sierra Vista', 'Sparks', 'Spokane', 'Springfield', 'Stockton', 'Sunnyvale', 'Temecula', 'Tempe', 'Thornton', 'Thousand Oaks', 'Tigard', 'Torrance', 'Tucson', 'Twin Falls', 'Vallejo', 'Vancouver', 'Visalia', 'West Jordan', 'Westminster', 'Whittier', 'Woodland', 'Yucaipa', 'Yuma']}

#Map countries to cities
country_to_cities = {'Argentina': ['Avellaneda', 'Bahía Blanca', 'Buenos Aires', 'Cipolletti', 'Comodoro Rivadavia', 'Concepción del Uruguay', 'Corrientes', 'Córdoba', 'Esquina', 'Junín', 'La Plata', 'La Rioja', 'Mar del Plata', 'Mendoza', 'Neuquén', 'Paraná', 'Posadas', 'Presidencia Roque Sáenz Peña', 'Quilmes', 'Resistencia', 'Rosario', 'Salta', 'San Fernando del Valle de Catamarca', 'San Juan', 'San Justo', 'San Luis', 'San Nicolás de los Arroyos', 'San Rafael', 'San Salvador de Jujuy', 'Santa Fe', 'Santa Rosa', 'Santiago del Estero', 'Tartagal'], 'Belice': ['San Ignacio'], 'Bolivia': ['Cochabamba', 'La Paz', 'Oruro', 'Potosí', 'Riberalta', 'Santa Cruz de la Sierra', 'Sucre', 'Trinidad', 'Yacuiba'], 'Brasil': ['Abreu e Lima', 'Altamira', 'Americana', 'Ananindeua', 'Andradina', 'Anápolis', 'Apucarana', 'Aracaju', 'Aracati', 'Araguaína', 'Arapiraca', 'Arapongas', 'Araranguá', 'Araraquara', 'Araucária', 'Araçatuba', 'Arcoverde', 'Ariquemes', 'Açu', 'Bagé', 'Balneário Camboriú', 'Barbacena', 'Barra Mansa', 'Barra do Piraí', 'Barreiras', 'Barreirinhas', 'Barretos', 'Barueri', 'Bayeux', 'Belo Horizonte', 'Bento Gonçalves', 'Betim', 'Bezerros', 'Birigui', 'Blumenau', 'Boa Esperança', 'Boa Vista', 'Bom Jesus da Lapa', 'Bragança Paulista', 'Brasília', 'Brumado', 'Buriticupu', 'Cabo Frio', 'Cabo de Santo Agostinho', 'Cajazeiras', 'Camaragibe', 'Camaçari', 'Cambé', 'Camocim', 'Campina Grande', 'Campo Grande', 'Campo Limpo Paulista', 'Canoas', 'Caraguatatuba', 'Carapicuíba', 'Cassilândia', 'Castanhal', 'Catalão', 'Catanduva', 'Caucaia', 'Caxias do Sul', 'Caçador', 'Chapecó', 'Cidade Ocidental', 'Coari', 'Colombo', 'Conselheiro Lafaiete', 'Contagem', 'Cotia', 'Crato', 'Criciúma', 'Cruz das Almas', 'Cruzeiro', 'Cruzeiro do Sul', 'Cubatão', 'Cuiabá', 'Curitiba', 'Diadema', 'Divinópolis', 'Dourados', 'Duque de Caxias', 'Erechim', 'Eunápolis', 'Farroupilha', 'Feira de Santana', 'Floriano', 'Fortaleza', 'Franca', 'Francisco Beltrão', 'Francisco Morato', 'Franco da Rocha', 'Garanhuns', 'Gaspar', 'Goiânia', 'Grajaú', 'Gravataí', 'Gravatá', 'Guanambi', 'Guarapari', 'Guarapuava', 'Guaratinguetá', 'Guarujá', 'Guarulhos', 'Gurupi', 'Ibirité', 'Ibiúna', 'Igarassu', 'Ijuí', 'Ilhéus', 'Indaial', 'Indaiatuba', 'Ipatinga', 'Itaituba', 'Itajaí', 'Itamaraju', 'Itapecerica da Serra', 'Itapecuru Mirim', 'Itapetininga', 'Itapeva', 'Itapevi', 'Itaúna', 'Itu', 'Ituiutaba', 'Jaboticabal', 'Jacareí', 'Jacobina', 'Jataí', 'Jaú', 'Jequié', 'Ji-Paraná', 'Joinville', 'José Bonifácio', 'João Pessoa', 'Juazeiro', 'Juiz de Fora', 'Jundiaí', 'Jurema', 'Lajeado', 'Lençóis Paulista', 'Limeira', 'Limoeiro do Norte', 'Linhares', 'Lins', 'Londrina', 'Lorena', 'Macapá', 'Maceió', 'Manacapuru', 'Manaus', 'Maringá', 'Mauá', 'Mococa', 'Mogi das Cruzes', 'Montes Claros', 'Mossoró', 'Natal', 'Navegantes', 'Niterói', 'Nova Serrana', 'Novo Cruzeiro', 'Novo Gama', 'Oriximiná', 'Osasco', 'Palhoça', 'Palmares', 'Paracatu', 'Paranaguá', 'Parintins', 'Passo Fundo', 'Passos', 'Pato Branco', 'Patrocínio', 'Paulista', 'Paço do Lumiar', 'Pelotas', 'Penedo', 'Petrópolis', 'Pilar', 'Pindamonhangaba', 'Pinheiro', 'Pirapora', 'Ponte Nova', 'Pontes e Lacerda', 'Porto Alegre', 'Pouso Alegre', 'Poços de Caldas', 'Praia Grande', 'Presidente Dutra', 'Presidente Prudente', 'Quixadá', 'Recife', 'Registro', 'Resende', 'Ribeirão Preto', 'Rio Branco', 'Rio Grande', 'Rolândia', 'Rondonópolis', 'Salvador', 'Santa Cruz do Sul', 'Santa Helena', 'Santa Rosa', 'Santana de Parnaíba', 'Santarém', 'Santo André', 'Santos', 'Sapucaia do Sul', 'Senhor do Bonfim', 'Seropédica', 'Serra', 'Simões Filho', 'Sinop', 'Sobral', 'Sorocaba', 'Sorriso', 'Sousa', 'Sumaré', 'Surubim', 'São Benedito', 'São Bernardo do Campo', 'São Gonçalo', 'São José dos Campos', 'São Leopoldo', 'São Luís', 'São Miguel dos Campos', 'São Paulo', 'São Pedro da Aldeia', 'São Vicente', 'Taboão da Serra', 'Tatuí', 'Taubaté', 'Teresina', 'Teresópolis', 'Tianguá', 'Toledo', 'Tupã', 'Uberaba', 'Uberlândia', 'Umuarama', 'Uruguaiana', 'Vacaria', 'Valinhos', 'Valparaíso de Goiás', 'Vassouras', 'Vespasiano', 'Vilhena', 'Vitória', 'Vitória da Conquista', 'Vitória de Santo Antão', 'Votuporanga', 'Várzea Grande', 'Águas Lindas de Goiás'], 'Chile': ['Antofagasta', 'Arica', 'Calama', 'Chillán', 'Copiapó', 'Iquique', 'La Pintana', 'Los Ángeles', 'Osorno', 'Puente Alto', 'Puerto Montt', 'Punta Arenas', 'Rancagua', 'San Antonio', 'San Bernardo', 'Santiago de Chile', 'Talcahuano', 'Valparaíso', 'Villa Alemana', 'Viña del Mar'], 'Colombia': ['Apartadó', 'Arauca', 'Armenia', 'Barranquilla', 'Bello', 'Bogotá', 'Bucaramanga', 'Cartagena', 'Cartago', 'Ciénaga', 'Cúcuta', 'Dos Quebradas', 'Duitama', 'Envigado', 'Facatativá', 'Florencia', 'Floridablanca', 'Girón', 'Ibagué', 'Ipiales', 'Jamundí', 'Los Patios', 'Malambo', 'Manizales', 'Medellín', 'Montenegro', 'Montería', 'Mosquera', 'Neiva', 'Ocaña', 'Palmira', 'Pasto', 'Pereira', 'Piedecuesta', 'Pitalito', 'Quibdó', 'Sabanalarga', 'Santa Marta', 'Soacha', 'Sogamoso', 'Soledad', 'Valledupar', 'Villavicencio', 'Yopal'], 'Costa Rica': ['Nicoya'], 'Ecuador': ['Cuenca', 'Guayaquil', 'Portoviejo', 'Quevedo', 'Quito', 'Santo Domingo de los Colorados'], 'El Salvador': ['Antiguo Cuscatlán', 'Apopa', 'Cuscatancingo', 'Delgado', 'Ilopango', 'Mejicanos', 'San Martín', 'San Salvador', 'Santa Ana', 'Sonsonate', 'Soyapango'], 'Estados Unidos': ['Akron', 'Albuquerque', 'Alexandria', 'Allentown', 'Altoona', 'Anaheim', 'Andover', 'Antioch', 'Apopka', 'Apple Valley', 'Arlington', 'Arvada', 'Asheville', 'Athens', 'Atlanta', 'Atlantic City', 'Auburn', 'Aurora', 'Avondale', 'Bakersfield', 'Baltimore', 'Bangor', 'Bayonne', 'Belleville', 'Bellevue', 'Bellingham', 'Bethlehem', 'Beverly', 'Billings', 'Boca Raton', 'Boise', 'Bossier City', 'Bowling Green', 'Boynton Beach', 'Bozeman', 'Brentwood', 'Bridgeton', 'Bristol', 'Broomfield', 'Buffalo', 'Bullhead City', 'Burbank', 'Burlington', 'Caldwell', 'Camarillo', 'Cambridge', 'Carlsbad', 'Cary', 'Chandler', 'Charlotte', 'Charlottesville', 'Chattanooga', 'Chesapeake', 'Chester', 'Chico', 'Chula Vista', 'Cincinnati', 'Citrus Heights', 'Clarksville', 'Cleveland', 'Clifton', 'Clinton', 'Clovis', 'Coachella', 'Colorado Springs', 'Columbia', 'Columbus', 'Commerce City', 'Concord', 'Conway', 'Coral Springs', 'Costa Mesa', 'Covington', 'Cranston', 'Cuyahoga Falls', 'Danville', 'Davis', 'Daytona Beach', 'Decatur', 'Delray Beach', 'Deltona', 'Denver', 'Des Moines', 'Dover', 'Draper', 'Dublín', 'Durham', 'East Orange', 'East Point', 'Edmonds', 'El Cajon', 'Elyria', 'Encinitas', 'Englewood', 'Escondido', 'Eugene', 'Everett', 'Fairfield', 'Farmington', 'Fayetteville', 'Florence', 'Fort Collins', 'Fort Lauderdale', 'Franklin', 'Freeport', 'Fresno', 'Gaithersburg', 'Gastonia', 'Georgetown', 'Gilbert', 'Glendale', 'Great Falls', 'Greensboro', 'Greenville', 'Gresham', 'Grove City', 'Gulfport', 'Hackensack', 'Hamilton', 'Hampton', 'Harrisonburg', 'Hattiesburg', 'Helena', 'Hempstead', 'Henderson', 'Hendersonville', 'Hesperia', 'Hialeah', 'Hickory', 'Hillsboro', 'Hollywood', 'Holyoke', 'Homestead', 'Hoover', 'Hot Springs', 'Huntington Beach', 'Huntsville', 'Inglewood', 'Jackson', 'Jacksonville', 'Jamestown', 'Johnson City', 'Jonesboro', 'Jupiter', 'Kenner', 'Kent', 'Kissimmee', 'Knoxville', 'La Mesa', 'Lafayette', 'Laguna Niguel', 'Lake Charles', 'Lake Elsinore', 'Lake Forest', 'Lakeland', 'Lakewood', 'Lancaster', 'Las Cruces', 'Las Vegas', 'Laurel', 'Lawrence', 'Layton', 'Lehi', 'Leominster', 'Lewiston', 'Linden', 'Lindenhurst', 'Little Rock', 'Lodi', 'Logan', 'Long Beach', 'Longmont', 'Longview', 'Lorain', 'Los Angeles', 'Louisville', 'Loveland', 'Lowell', 'Líbano', 'Macon', 'Malden', 'Manchester', 'Manteca', 'Margate', 'Marietta', 'Marion', 'Marlborough', 'Marysville', 'Mason', 'Medford', 'Medina', 'Memphis', 'Mentor', 'Meriden', 'Meridian', 'Mesa', 'Miami', 'Middletown', 'Milford', 'Miramar', 'Mission Viejo', 'Missoula', 'Mobile', 'Modesto', 'Monroe', 'Montebello', 'Montgomery', 'Moreno Valley', 'Morgan Hill', 'Morristown', 'Mount Pleasant', 'Mount Vernon', 'Murfreesboro', 'Murray', 'Murrieta', 'Nashua', 'Nashville', 'New Bedford', 'New Brunswick', 'New Rochelle', 'New York City', 'Newark', 'Newport News', 'Niagara Falls', 'North Charleston', 'North Las Vegas', 'North Miami', 'Norwich', 'Oakland', 'Oceanside', 'Olympia', 'Ontario', 'Orange', 'Orem', 'Orlando', 'Ormond Beach', 'Owensboro', 'Oxnard', 'Palm Coast', 'Parker', 'Parma', 'Pasadena', 'Pasco', 'Passaic', 'Paterson', 'Pembroke Pines', 'Pensacola', 'Peoria', 'Perth Amboy', 'Philadelphia', 'Phoenix', 'Pico Rivera', 'Pine Bluff', 'Plainfield', 'Plantation', 'Pleasant Grove', 'Pocatello', 'Pomona', 'Pompano Beach', 'Port Saint Lucie', 'Portland', 'Providence', 'Provo', 'Pueblo', 'Quincy', 'Raleigh', 'Rancho Cucamonga', 'Reading', 'Redding', 'Redlands', 'Redmond', 'Redondo Beach', 'Redwood City', 'Reno', 'Renton', 'Revere', 'Richmond', 'Rio Rancho', 'Riverside', 'Rochester', 'Rock Hill', 'Rockville', 'Rome', 'Roseville', 'Roswell', 'Sacramento', 'Saint Petersburg', 'Salem', 'Salinas', 'Salt Lake City', 'San Bernardino', 'San Clemente', 'San Diego', 'San Francisco', 'San Gabriel', 'San Jose', 'San Luis Obispo', 'San Mateo', 'Sandy Springs', 'Sanford', 'Santa Ana', 'Santa Barbara', 'Santa Clara', 'Santa Fe', 'Santa Maria', 'Scottsdale', 'Seattle', 'Shelton', 'Sierra Vista', 'Smyrna', 'Southaven', 'Sparks', 'Spokane', 'Springdale', 'Springfield', 'Stockton', 'Suffolk', 'Summerville', 'Sunnyvale', 'Tallahassee', 'Tamarac', 'Tampa', 'Temecula', 'Tempe', 'Texarkana', 'Thomasville', 'Thornton', 'Thousand Oaks', 'Tigard', 'Toledo', 'Torrance', 'Troy', 'Tucson', 'Tuscaloosa', 'Twin Falls', 'Utica', 'Vallejo', 'Vancouver', 'Vineland', 'Virginia Beach', 'Visalia', 'Warner Robins', 'Warwick', 'Washington', 'Waterbury', 'Watertown', 'Waynesboro', 'West Jordan', 'West Palm Beach', 'Westfield', 'Westminster', 'Wheeling', 'Whittier', 'Wilmington', 'Wilson', 'Woodland', 'Woodstock', 'Woonsocket', 'Yonkers', 'York', 'Yucaipa', 'Yuma'], 'Guatemala': ['Amatitlán', 'Chimaltenango', 'Chinautla', 'Escuintla', 'Guatemala City', 'Huehuetenango', 'Mixco', 'Petapa', 'Quetzaltenango', 'Villa Canales', 'Villa Nueva'], 'Guayana Francesa': ['Cayenne'], 'Guyana': ['Linden'], 'Honduras': ['Choloma', 'Choluteca', 'El Progreso', 'La Ceiba', 'San Pedro Sula', 'Tegucigalpa'], 'México': ['Acayucan', 'Acuña', 'Acámbaro', 'Altotonga', 'Apatzingán de la Constitución', 'Apodaca', 'Atlixco', 'Azcapotzalco', 'Cadereyta', 'Campeche', 'Cancún', 'Celaya', 'Chetumal', 'Chihuahua', 'Chilpancingo', 'Cholula', 'Ciudad del Carmen', 'Coacalco', 'Coatzacoalcos', 'Colima', 'Coyoacán', 'Cuajimalpa', 'Cuautitlán', 'Cuernavaca', 'Culiacán', 'Córdoba', 'Delicias', 'Durango', 'Ensenada', 'Fresnillo de González Echeverría', 'Frontera', 'Garza García', 'General Escobedo', 'Guadalajara', 'Guamúchil', 'Guanajuato', 'Guasave', 'Guaymas', 'Guzmán', 'Gómez Palacio', 'Hermosillo', 'Heroica Zitácuaro', 'Hidalgo', 'Huixquilucan', 'Iguala', 'Irapuato', 'Ixtapaluca', 'Jiutepec', 'Juárez', 'La Paz', 'Lagos de Moreno', 'León', 'Linares', 'Los Mochis', 'Lázaro Cárdenas', 'Madero', 'Manzanillo', 'Matehuala', 'Melchor Ocampo', 'Metepec', 'Mexicali', 'Mexico City', 'Miguel Hidalgo', 'Milpa Alta', 'Miramar', 'Monclova', 'Monterrey', 'Morelia', 'Mérida', 'Nicolás Romero', 'Nuevo Laredo', 'Obregón', 'Ocotlán', 'Orizaba', 'Piedras Negras', 'Poza Rica de Hidalgo', 'Progreso', 'Puebla', 'Puerto Vallarta', 'Querétaro', 'Reynosa', 'Rosarito', 'Río Bravo', 'Sahuayo de José María Morelos', 'Salamanca', 'Salina Cruz', 'Saltillo', 'San Andrés Tuxtla', 'San Cristóbal de Las Casas', 'San Francisco del Rincón', 'San Juan del Río', 'San Luis Potosí', 'San Luis Río Colorado', 'San Pablo de las Salinas', 'Santa Catarina', 'Silao', 'Soledad Díez Gutiérrez', 'Tampico', 'Tapachula', 'Tecomán', 'Tehuacán', 'Temixco', 'Tepic', 'Teziutlán', 'Tijuana', 'Tlalnepantla', 'Tlalpan', 'Tlaquepaque', 'Toluca', 'Torreón', 'Tulancingo', 'Tuxtla Gutiérrez', 'Valle Hermoso', 'Valles', 'Veracruz', 'Victoria', 'Villa Frontera', 'Villahermosa', 'Zacatecas', 'Zapopan', 'Zihuatanejo'], 'Nicaragua': ['Chinandega', 'Estelí', 'Granada', 'León', 'Managua', 'Masaya', 'Matagalpa', 'Tipitapa'], 'Panamá': ['Arraiján', 'Colón', 'David', 'La Chorrera', 'Panama City', 'San Miguelito'], 'Paraguay': ['Asunción', 'Fernando de la Mora', 'Lambaré', 'San Lorenzo'], 'Perú': ['Arequipa', 'Ayacucho', 'Barranca', 'Cajamarca', 'Callao', 'Chiclayo', 'Chimbote', 'Chincha Alta', 'Huancayo', 'Huaraz', 'Ilo', 'Iquitos', 'Juliaca', 'Lima', 'Paita', 'Piura', 'Pucallpa', 'Puno', 'Talara', 'Trujillo'], 'Surinam': ['Paramaribo'], 'Uruguay': ['Las Piedras', 'Montevideo', 'Paysandú', 'Rivera'], 'Venezuela': ['Acarigua', 'Barcelona', 'Barquisimeto', 'Baruta', 'Bolívar', 'Cabimas', 'Cagua', 'Calabozo', 'Caracas', 'Carora', 'Catia La Mar', 'Charallave', 'Cumaná', 'Cúa', 'El Limón', 'El Tigre', 'Guacara', 'Guanare', 'Guarenas', 'Guatire', 'Guayana', 'Maracaibo', 'Maracay', 'Maturín', 'Mérida', 'Palo Negro', 'Petare', 'Porlamar', 'Puerto La Cruz', 'San Carlos del Zulia', 'San Cristóbal', 'San José de Guanipa', 'Tinaquillo', 'Turmero', 'Valencia', 'Valle de La Pascua', 'Yaritagua']}


# In[87]:


#pip install streamlit


# In[88]:


import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product
import joblib


# Load the model pipeline and threshold
final_model_pipeline = joblib.load("finalmodel2.pkl")
optimal_threshold = 0.45451189375129714


# Define the app
st.title("Late Delivery Risk Prediction")

#Late Risk Delivery Trends monitoring chart
st.header("Identifying deliveries with high risk of being late")
# Variable values
shipping_modes = ["First Class", "Same Day", "Second Class", "Standard Class"]
payment_types = ["PAYMENT", "TRANSFER", "DEBIT", "CASH"]
order_regions = ['Central America', 'South America', 'East of USA', 'South of  USA ', 'West of USA ']


# Generate combinations
data = []

for region, countries in region_to_countries.items():
    for country in countries:
        cities = country_to_cities.get(country, [])
        for city in cities:
            for shipping_mode in shipping_modes:
                for type in payment_types:
                    data.append((shipping_mode, type, city, country, region))

# Convert to DataFrame
combination_df = pd.DataFrame(data, columns=["shipping_mode", "type", "order_city", "order_country", "order_region"])

# Predict late delivery risk for each combination
# Select only the relevant columns
input_features = combination_df[["shipping_mode", "type", "order_country"]]

# Make predictions using the model pipeline
predictions = final_model_pipeline.predict_proba(input_features)[:, 1]

combination_df["risk_score_late_delivery"] = predictions

# Add a risk category based on the threshold
combination_df["risk_category"] = np.where(combination_df["risk_score_late_delivery"] >= optimal_threshold, "High Risk", "Low Risk")

import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta


# Visualization: Heatmap Plot of Late Delivery Risk

# Streamlit dropdown for order_region
selected_region = st.selectbox(
    "Select an Order Region:",
    options=["All"] + combination_df["order_region"].unique().tolist()
)


# Filter countries based on selected region
if selected_region != "All":
    valid_countries = region_to_countries.get(selected_region, [])
    country_options = ["All"] + [country for country in valid_countries if country in combination_df["order_country"].unique()]
else:
    country_options = ["All"] + combination_df["order_country"].unique().tolist()

# Streamlit dropdown for order_country
selected_country = st.selectbox(
    "Select an Order Country:",
    options=country_options
)

# Filter data based on selected region and country
filtered_df = combination_df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["order_region"] == selected_region]

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["order_country"] == selected_country]

countrynamechoropleth = country_mapping = {
    'Argentina': 'Argentina',
    'Belice': 'Belize',
    'Bolivia': 'Bolivia',
    'Brasil': 'Brazil',
    'Chile': 'Chile',
    'Colombia': 'Colombia',
    'Costa Rica': 'Costa Rica',
    'Ecuador': 'Ecuador',
    'El Salvador': 'El Salvador',
    'Estados Unidos': 'United States',
    'Guatemala': 'Guatemala',
    'Guayana Francesa': 'French Guiana',
    'Guyana': 'Guyana',
    'Honduras': 'Honduras',
    'México': 'Mexico',
    'Nicaragua': 'Nicaragua',
    'Panamá': 'Panama',
    'Paraguay': 'Paraguay',
    'Perú': 'Peru',
    'Surinam': 'Suriname',
    'Uruguay': 'Uruguay',
    'Venezuela': 'Venezuela'
}


# Calculate average risk score by country
average_risk_by_country = combination_df.groupby("order_country")["risk_score_late_delivery"].mean().reset_index()
average_risk_by_country = average_risk_by_country.merge(combination_df[["order_country", "order_region"]].drop_duplicates(), on="order_country", how="left")
average_risk_by_country["chlorpleth_country"] = average_risk_by_country["order_country"].map(countrynamechoropleth)

# Save combination_df and average_risk_by_country as CSV
combination_df.to_csv('combination_df.csv', index=False)
average_risk_by_country.to_csv('average_risk_by_country.csv', index=False)
# Filter the average risk score DataFrame based on selections
filtered_avg_risk_df = average_risk_by_country.copy()

if selected_region != "All":
    filtered_avg_risk_df = filtered_avg_risk_df[filtered_avg_risk_df["order_region"] == selected_region]
else:
    filtered_avg_risk_df = average_risk_by_country
if selected_country != "All":
    filtered_avg_risk_df = filtered_avg_risk_df[filtered_avg_risk_df["order_country"] == selected_country]
else:
    filtered_avg_risk_df = filtered_avg_risk_df[filtered_avg_risk_df["order_region"] == selected_region]
    


st.write("Late Delivery Risk by Region and Country")

# Choropleth map logic for "All" or specific region
if selected_region == "All":
    # Single map for all regions
    figcm = px.choropleth(
        filtered_avg_risk_df,
        locations="chlorpleth_country",
        locationmode="country names",
        color="risk_score_late_delivery",
        hover_name="order_country",
        color_continuous_scale="Reds",
        title="Late Delivery Risk by Country"
    )
else:
    # Faceted map for specific region
    figcm = px.choropleth(
        filtered_avg_risk_df,
        locations="chlorpleth_country",
        locationmode="country names",
        color="risk_score_late_delivery",
        hover_name="order_country",
        color_continuous_scale="Reds",
        title="Late Delivery Risk by Country",
        facet_col="order_region"
    )

st.plotly_chart(figcm)



# Create a pivot table for the heatmap
heatmap_data = filtered_df.pivot_table(
    index="shipping_mode",
    columns="type",
    values="risk_score_late_delivery",
    aggfunc="mean"  # Aggregate mean risk score for combinations
).fillna(0)  # Replace NaN with 0

# Create a heatmap
fig = px.imshow(
    heatmap_data,
    labels=dict(x="Payment Type", y="Shipping Mode", color="Risk Score"),
    color_continuous_scale="Reds",  # Choose a color scale
    title=f"Heatmap: Risk Score by Shipping Mode and Payment Type (Region: {selected_region}, Country: {selected_country})"
)
st.plotly_chart(fig)


# Display the top risky combinations
st.write("Top 10 Risky Combinations")
filtered_risky_combinations = filtered_df.sort_values("risk_score_late_delivery", ascending=False).head(10)
st.dataframe(filtered_risky_combinations)

# After displaying the heatmap
st.subheader(f"Insights and Recommendations for Region: {selected_region}, Country: {selected_country}")

# Generate insights based on the heatmap
high_risk_modes = heatmap_data.idxmax(axis=0).to_dict()
high_risk_payment_types = heatmap_data.idxmax(axis=1).to_dict()

st.write("### Recommendations:")
for payment_type, shipping_mode in high_risk_modes.items():
    if payment_type in heatmap_data.columns:
        try:
            low_risk_shipping_mode = heatmap_data[payment_type].idxmin()
            st.write(f"- **Recommendation for Shipping Mode: {shipping_mode}:** Switch to '{low_risk_shipping_mode}' shipping mode for reduced risks.")
        except Exception as e:
            st.write(f"- Unable to determine a lower-risk shipping mode for Payment Type: {payment_type}.")
for shipping_mode, payment_type in high_risk_payment_types.items():
    if shipping_mode in heatmap_data.index:
        try:
            low_risk_payment_type = heatmap_data.loc[shipping_mode].idxmin()
            st.write(f"- **Recommendation for Payment Type: {payment_type}:** Switch to '{low_risk_payment_type}' payment type for reduced risks.")
        except Exception as e:
            st.write(f"- Unable to determine a lower-risk payment type for Shipping Mode: {shipping_mode}.")

st.write("### Potential Reasons for High Risk:")
st.write("- Higher risks may be due to longer transit times for specific shipping modes.")
st.write("- Payment delays or processing times associated with certain payment methods.")
st.write("- Geographical challenges in certain regions.")


# Simulate 100 orders
np.random.seed(42)
regions = np.random.choice(list(region_to_countries.keys()), size=100)
countries = [np.random.choice(region_to_countries[region]) for region in regions]
cities = [np.random.choice(country_to_cities[country]) for country in countries]
order_statuses = ["PENDING_PAYMENT", "PENDING", "PROCESSING", "ON_HOLD", "COMPLETE", "CLOSED", "SUSPECTED_FRAUD", "CANCELED", "PAYMENT_REVIEW"]
shipping_modes = ["First Class", "Same Day", "Second Class", "Standard Class"]
payment_types = ["PAYMENT", "TRANSFER", "DEBIT", "CASH"]
products = [f"Product {i}" for i in range(1, 21)]

simulated_data = pd.DataFrame({
    "order_id": [f"ORD-{i:03d}" for i in range(1, 101)],
    "order_region": regions,
    "order_country": countries,
    "order_city": cities,
    "order_status": np.random.choice(order_statuses, 100),
    "shipping_mode": np.random.choice(shipping_modes, 100),
    "type": np.random.choice(payment_types, 100),
    "product_name": np.random.choice(products, 100),
    "order_date_(dateorders)": [datetime(2023, 1, 1) + timedelta(days=np.random.randint(1, 365)) for _ in range(100)]
})


# Predict late delivery risk based on shipping mode
simulated_data["late_delivery_risk"] = final_model_pipeline.predict_proba(simulated_data[["shipping_mode","order_status","type","order_country"]])[:, 1]
simulated_data["risk_category"] = np.where(simulated_data["late_delivery_risk"] >= optimal_threshold, "High Risk", "Low Risk")

# User selection
st.header("Risk of Late Delivery for current orders")

# Region selection
selected_region = st.selectbox("Select Order Region", ["All"] + list(region_to_countries.keys()))

if selected_region != "All":
    # Filter countries based on selected region
    region_countries = region_to_countries[selected_region]
    filtered_data = simulated_data[simulated_data["order_region"] == selected_region]
else:
    # When "All" is selected for the region, do not filter the DataFrame and show "All" in the country dropdown
    region_countries = ["All"]
    filtered_data = simulated_data

# Country selection
selected_country = st.selectbox("Select Order Country", list(region_countries))

if selected_country != "All":
    # Get regions for the selected country
    country_regions = region_countries[selected_country]
    selected_region = st.selectbox("Select Region", country_regions)

    if selected_region != "All":
        # Get cities for the selected region
        country_cities = country_to_cities[selected_region]
        filtered_data = filtered_data[filtered_data["order_region"] == selected_region]
    else:
        country_cities = ["All"]
        filtered_data = filtered_data[filtered_data["order_country"] == selected_country]
else:
    country_cities = ["All"]
    filtered_data = filtered_data

# City selection
selected_city = st.selectbox("Select Order City", country_cities)

if selected_city != "All":
    # Further filter data if a specific city is selected
    filtered_data = filtered_data[filtered_data["order_city"] == selected_city]
else:
    filtered_data = filtered_data

# Display the filtered data
st.write("Filtered Order Data")
st.dataframe(filtered_data)

# Pie chart for risk category division
st.subheader("Order Division by Risk Category")
st.write(f"**Optimal Threshold for High Risk**: {optimal_threshold:.2f}")

risk_counts = filtered_data["risk_category"].value_counts()
fig1, ax1 = plt.subplots(figsize=(2, 2))
ax1.pie(
    risk_counts, labels=risk_counts.index, autopct="%1.1f%%", colors=["red", "green"], textprops={'fontsize': 5}
)
ax1.set_title("Distribution of order based on risk of delivery compared to optimal threshold ")
st.pyplot(fig1)

# Display high-risk orders
st.subheader("List of High-Risk Orders")
high_risk_orders = filtered_data[filtered_data["risk_category"] == "High Risk"]
st.dataframe(high_risk_orders)


# Order selection
selected_order_id = st.selectbox("Select Order ID", filtered_data["order_id"])
selected_order = filtered_data[filtered_data["order_id"] == selected_order_id]

# Display selected order details
if not selected_order.empty:
    st.write("Selected Order Details:")
    st.dataframe(selected_order)

    risk_score = selected_order["late_delivery_risk"].values[0]
    risk_category = "High Risk" if risk_score >= optimal_threshold else "Low Risk"
    st.write(f"**Late Delivery Risk Prediction:** {risk_category} ({risk_score:.2f})")
else:
    st.warning("No order selected.")

# Define plot function
def plot_selected_order_trends(data, selected_order, fig):
    """Plots trends based on the selected order attributes."""
    # Extract the relevant attributes
    shipping_mode = selected_order["shipping_mode"].iloc[0]
    payment_type = selected_order["type"].iloc[0]

    # Ensure datetime and quarters
    data["Quarter"] = pd.to_datetime(data["order_date_(dateorders)"]).dt.to_period("Q")
    all_quarters = pd.period_range("2015Q1", "2017Q4", freq="Q")

    # Subplot 1: Stacked bar chart for late vs. on-time deliveries (shipping mode)
    ax3 = fig.add_subplot(3, 2, 3)
    shipping_data = data[data["shipping_mode"] == shipping_mode]
    shipping_quarterly = shipping_data.groupby(["Quarter", "late"]).size().unstack(fill_value=0)
    shipping_quarterly = shipping_quarterly.reindex(all_quarters, fill_value=0)
    percentage_shipping = shipping_quarterly.div(shipping_quarterly.sum(axis=1), axis=0) * 100
    percentage_shipping.plot(kind="bar", stacked=True, color=["red", "green"], ax=ax3)
    ax3.set_title(f"% Late vs. On-Time Deliveries (Shipping Mode: {shipping_mode})")
    ax3.set_xlabel("Quarter")
    ax3.set_ylabel("Percentage")

    # Subplot 2: Average number of days late (shipping mode)
    ax4 = fig.add_subplot(3, 2, 4)
    avg_days_shipping = shipping_data[shipping_data["late"] == True].groupby("Quarter")["late?"].mean()
    avg_days_shipping = avg_days_shipping.reindex(all_quarters, fill_value=0)
    avg_days_shipping.plot(kind="bar", color="red", ax=ax4)
    ax4.set_title(f"Average Days Late (Shipping Mode: {shipping_mode})")
    ax4.set_xlabel("Quarter")
    ax4.set_ylabel("Average Days Late")

    # Subplot 3: Stacked bar chart for late vs. on-time deliveries (payment type)
    ax5 = fig.add_subplot(3, 2, 5)
    payment_data = data[data["type"] == payment_type]
    payment_quarterly = payment_data.groupby(["Quarter", "late"]).size().unstack(fill_value=0)
    payment_quarterly = payment_quarterly.reindex(all_quarters, fill_value=0)
    percentage_payment = payment_quarterly.div(payment_quarterly.sum(axis=1), axis=0) * 100
    percentage_payment.plot(kind="bar", stacked=True, color=["red", "green"], ax=ax5)
    ax5.set_title(f"% Late vs. On-Time Deliveries (Payment Type: {payment_type})")
    ax5.set_xlabel("Quarter")
    ax5.set_ylabel("Percentage")

    # Subplot 4: Average number of days late (payment type)
    ax6 = fig.add_subplot(3, 2, 6)
    avg_days_payment = payment_data[payment_data["late"] == True].groupby("Quarter")["late?"].mean()
    avg_days_payment = avg_days_payment.reindex(all_quarters, fill_value=0)
    avg_days_payment.plot(kind="bar", color="red", ax=ax6)
    ax6.set_title(f"Average Days Late (Payment Type: {payment_type})")
    ax6.set_xlabel("Quarter")
    ax6.set_ylabel("Average Days Late")

# Create the figure and plot
fig = plt.figure(figsize=(15, 15))
plot_selected_order_trends(df, selected_order, fig)
plt.subplots_adjust(hspace=0.4)  # Increase the vertical spacing between plots
st.pyplot(fig)
# For the selected order
if not selected_order.empty:
    st.subheader("Recommendations for Selected Order")
    # Extract selected order details
    selected_shipping_mode = selected_order["shipping_mode"].iloc[0]
    selected_payment_type = selected_order["type"].iloc[0]
    selected_risk_score = selected_order["late_delivery_risk"].iloc[0]

    # Provide recommendations
    if selected_risk_score >= optimal_threshold:
        st.write(f"The selected order has a **High Risk** of late delivery (Risk Score: {selected_risk_score:.2f}).")
        
        # Check and recommend lower-risk shipping mode
        if selected_payment_type in heatmap_data.columns:
            recommended_shipping = heatmap_data[selected_payment_type].idxmin()
            st.write(f"- **Switch to '{recommended_shipping}' shipping mode to reduce risk'.**")
        
        # Check and recommend lower-risk payment type
        if selected_shipping_mode in heatmap_data.index:
            recommended_payment = heatmap_data.loc[selected_shipping_mode].idxmin()
            st.write(f"- **Switch to '{recommended_payment}' payment type to reduce risk'.**")
    else:
        st.write("The selected order has a **Low Risk** of late delivery. No changes recommended.")

# Display warnings or further recommendations
st.write("**General Advice:**")
st.write("- Streamline payment processing systems to minimize delays.")
st.write("- Use real-time tracking for shipments in high-risk countries.")
st.write("- Offer expedited shipping options for time-sensitive deliveries.")
st.write("- Alert customers about potential delays due to external factors.")

#Simulating affect of recommendations

# Filter late orders
late_orders = simulated_data[simulated_data["risk_category"] == "High Risk"]

# Initialize lists to store results
recommended_changes = []
new_risk_scores_shipping = []
new_risk_scores_payment = []
new_risk_scores_both = []

# Iterate through late orders
for _, order in late_orders.iterrows():
    current_shipping_mode = order["shipping_mode"]
    current_payment_type = order["type"]

    # Recommend a new shipping mode and payment type
    recommended_shipping = heatmap_data.loc[:, current_payment_type].idxmin()
    recommended_payment = heatmap_data.loc[current_shipping_mode].idxmin()

    # Predict risk scores with updates
    updated_shipping_risk = heatmap_data.loc[recommended_shipping, current_payment_type]
    updated_payment_risk = heatmap_data.loc[current_shipping_mode, recommended_payment]
    updated_both_risk = heatmap_data.loc[recommended_shipping, recommended_payment]

    # Append results
    recommended_changes.append(
        {
            "order_id": order["order_id"],
            "current_shipping_mode": current_shipping_mode,
            "current_payment_type": current_payment_type,
            "recommended_shipping_mode": recommended_shipping,
            "recommended_payment_type": recommended_payment,
            "original_risk": order["late_delivery_risk"],
            "updated_shipping_risk": updated_shipping_risk,
            "updated_payment_risk": updated_payment_risk,
            "updated_both_risk": updated_both_risk,
        }
    )
    new_risk_scores_shipping.append(updated_shipping_risk)
    new_risk_scores_payment.append(updated_payment_risk)
    new_risk_scores_both.append(updated_both_risk)

# Create a DataFrame for recommendations
recommendations_df = pd.DataFrame(recommended_changes)

# Calculate % of late risk deliveries for each scenario
original_late_percentage = len(late_orders) / len(simulated_data) * 100
updated_shipping_late_percentage = (
    sum(np.array(new_risk_scores_shipping) >= optimal_threshold) / len(simulated_data) * 100
)
updated_payment_late_percentage = (
    sum(np.array(new_risk_scores_payment) >= optimal_threshold) / len(simulated_data) * 100
)
updated_both_late_percentage = (
    sum(np.array(new_risk_scores_both) >= optimal_threshold) / len(simulated_data) * 100
)

# Sort the recommendations DataFrame by original risk descending
recommendations_df = recommendations_df.sort_values(by="original_risk", ascending=False)

# Output results
st.subheader("Recommendations for Late Orders")
st.write("### Sorted Recommendations:")
st.dataframe(recommendations_df)

st.write("### Late Delivery Risk Percentages:")
st.write(f"- **Original Late Risk Deliveries**: {original_late_percentage:.2f}%")
st.write(f"- **% Late Risk Deliveries (Only Shipping Updated)**: {updated_shipping_late_percentage:.2f}%")
st.write(f"- **% Late Risk Deliveries (Only Payment Updated)**: {updated_payment_late_percentage:.2f}%")
st.write(f"- **% Late Risk Deliveries (Both Updated)**: {updated_both_late_percentage:.2f}%")

st.write("Overall recommendation is to update the payment type and shipping mode based on recommendation, otherwise prioritize the update of payment mode. Improve the payment infrastructure such that there are fewer transfer options, and more cash and debit payments. ")
