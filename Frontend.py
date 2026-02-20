import React, { useState } from 'react';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Select, SelectItem } from '@/components/ui/select';

const App = () => {
  const [selectedOption, setSelectedOption] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleOptionChange = (value) => {
    setSelectedOption(value);
  };

  const executeQuery = async () => {
    if (!selectedOption) {
      setMessage('⚠️ Por favor, seleccione una opción.');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const response = await axios.post(`http://localhost:5000/${selectedOption}`); // Ajusta la URL según tu backend
      if (response.status === 200) {
        setMessage(`✅ Consulta completada. Resultado: ${response.data.message}`);
      } else {
        setMessage('⚠️ Ocurrió un error al realizar la consulta.');
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('❌ Error al conectar con la API.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 flex flex-col items-center space-y-6">
      <Card className="w-full max-w-md">
        <CardContent className="space-y-4">
          <h2 className="text-xl font-bold">📋 Menú de Consultas</h2>

          <Select
            placeholder="Seleccione una opción"
            value={selectedOption}
            onChange={(e) => handleOptionChange(e.target.value)}
            className="w-full"
          >
            <SelectItem value="indicadores">Indicadores</SelectItem>
            <SelectItem value="salidasNoConformes">Salidas No Conformes</SelectItem>
            <SelectItem value="accionesMejora">Acciones Mejora</SelectItem>
            <SelectItem value="documentos">Documentos</SelectItem>
            <SelectItem value="riesgos">Riesgos</SelectItem>
          </Select>

          <Button
            onClick={executeQuery}
            disabled={loading}
            className="w-full"
          >
            {loading ? 'Procesando...' : 'Ejecutar Consulta'}
          </Button>

          {message && (
            <p className={`text-sm mt-4 ${message.includes('✅') ? 'text-green-600' : 'text-red-600'}`}>
              {message}
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default App;
