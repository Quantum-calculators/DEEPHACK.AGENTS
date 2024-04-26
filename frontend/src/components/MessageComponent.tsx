import { MessageBox } from './MessageBox';
import Plotly from "plotly.js";
import Plot from 'react-plotly.js';
import {BoxPlot, LinePlot, HeatMap} from "./PlotComponent"





export interface ChatHistory {
	result: {
		user: boolean, // если сообщение пользователя - true, ответ сервера - false
		UUID: string,
		date: string,
		Message: { 
			text: string,
			PlotType: string, // пустое поле, если user=true
			PlotData: {
				X: number[], // пустое поле, если user=true
				Y: number[], // пустое поле, если user=true
				Z: number[], // пустое поле, если user=true
				Styles: {
					Color: string, // пустое поле, если user=true
					PlotSize: number, // пустое поле, если user=true
				},
			},
		Error: string,
		}
	}[]
}


interface IMessageShowProps{
	story?: ChatHistory
}


export function MessageShow(props: IMessageShowProps){
	let output_element: JSX.Element[] = []
	props.story?.result.forEach(element => {
        output_element.push(

			<MessageBox
				is_user={element.user}
				date={element.date}
				message={element.Message.text}/>
		)
		if (element.Message.PlotType && !element.user){
			if (element.Message.PlotType === "box_and_whiskers"){
				output_element.push(
					<BoxPlot x={element.Message.PlotData.X} plot_size={2}/>
				)
			}
			if (element.Message.PlotType === "heatmap"){
				output_element.push(
					<HeatMap x={element.Message.PlotData.X} plot_size={2}/>
				)
			}
			if (element.Message.PlotType === "scatterplot"){
				output_element.push(
					<LinePlot x={element.Message.PlotData.X} y={element.Message.PlotData.Y} markers='markers' plot_size={2}/>
				)
			}
			if (element.Message.PlotType === "linear_plot"){
				output_element.push(
					<LinePlot x={element.Message.PlotData.X} y={element.Message.PlotData.Y} markers='lines' plot_size={2}/>
				)
			}
        }
	});
	return (
		<>
		{output_element}
		</>
	)
}