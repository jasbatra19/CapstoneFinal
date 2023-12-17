import React from "react";
import { Chart } from "react-google-charts";

const options = {
  title: "Questions answered",
  chartArea: { width: "50%" },
  hAxis: {
    title: "Total Questions",
    minValue: 0,
  },
  vAxis: {
    title: "Difficulty Level",
  },
};

const LineChart = ({ data }) => {
  return <Chart chartType="LineChart" width="100%" height="400px" data={data} options={options} />;
};

export default LineChart;
