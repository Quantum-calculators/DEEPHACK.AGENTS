import { MessageBox } from './MessageBox';
import Plotly from "plotly.js";
import Plot from 'react-plotly.js';


export {BoxPlot, LinePlot, HeatMap}


interface BoxPlotData {
    x: number[],
    plot_size: number,
}

function BoxPlot(props: BoxPlotData){
    return (
        <Plot
            data={[
            {
                x: props.x,
                type: 'box',
            },
            ]}
            layout={ {width: 320 * props.plot_size, height: 240 * props.plot_size, title: 'BoxPlot'} }
        />
    )
}


interface ScatterPlotData {
    x: number[],
    y: number[],
    markers: string, // lines, markers, lines+markers
    plot_size: number,
}

function LinePlot(props: ScatterPlotData){
    return (
        <Plot
            data={[
            {
                x: props.x,
                y: props.y,
                type: 'scatter',
                mode: 'lines',
                marker: {color: 'red'},
            },
            ]}
            layout={ {width: 320 * props.plot_size, height: 240 * props.plot_size, title: 'LinePlot'} }
        />
    )
}


interface HeatMapData {
    x: number[],
    plot_size: number,
}

function HeatMap(props: HeatMapData){
    return (
        <Plot
            data={[
                {
                    z: props.x,
                    type: 'heatmap',
                    marker: {color: 'red'},
                },
            ]}
            layout={ {width: 320 * props.plot_size, height: 240 * props.plot_size, title: 'HeatMap'} }
        />
    )
}

