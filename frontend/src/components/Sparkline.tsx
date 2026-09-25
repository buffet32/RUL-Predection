import { LineChart, Line, XAxis, YAxis, ResponsiveContainer } from 'recharts';

interface SparklineProps {
  data: number[];
  color?: string;
}

export default function Sparkline({ data, color = '#2563EB' }: SparklineProps) {
  const chartData = data.map((value, index) => ({ index, value }));

  return (
    <ResponsiveContainer width={100} height={40}>
      <LineChart data={chartData}>
        <XAxis 
          dataKey="index" 
          hide 
        />
        <YAxis 
          hide 
          domain={['dataMin', 'dataMax']}
        />
        <Line 
          type="monotone" 
          dataKey="value" 
          stroke={color} 
          strokeWidth={2} 
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
