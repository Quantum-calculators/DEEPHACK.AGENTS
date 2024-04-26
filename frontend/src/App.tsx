import './App.css';
import { useState, useEffect } from "react"
import moment from 'moment';
import SyncLoader from "react-spinners/SyncLoader";
import { ChatHistory, MessageShow } from './components/MessageComponent';
import { getCookie, setCookie } from 'typescript-cookie'


interface BotMessage {
	UUID: string,
	GigachainData: string,
	PlotType: string,
	PlotData: {
		X: number[],
		Y: number[],
		Z: number[],
		Styles: {
			Color: string,
			PlotSize: number
		}
	}
}


function App() {
	const [input_message, set_input_message] = useState("");
	const [bot_message, set_bot_message] = useState<BotMessage>()
	const [history, set_history] = useState<ChatHistory>()
	const [spinner, setSpinner] = useState(false);
	
	
	function send_message(){
		let input_message = (document.getElementById("InputMessageElement") as HTMLInputElement).value
		
		let user_message = {
			UUID: getCookie("uuid") as string,
			userData: input_message,
			error: "none"
		}

		let new_message = {
			user: true, // если сообщение пользователя - true, ответ сервера - false
			UUID: user_message.UUID,
			date: moment().format("hh:mm, DD.MM.YY"),
			Message: { 
				text: user_message.userData,
				PlotType: "", // пустое поле, если user=true
				PlotData: {
					X: [], // пустое поле, если user=true
					Y: [], // пустое поле, если user=true
					Z: [], // пустое поле, если user=true
					Styles: {
						Color: "", // пустое поле, если user=true
						PlotSize: 0, // пустое поле, если user=true
					},
				},
			Error: "",
			}
		}
		history?.result.push(
			new_message
		)
		set_input_message("")

		return user_message
	}

	function post(){
		let user_message = send_message()

		const requestOptionsStatApi = {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(user_message)
		};
		setSpinner(true)
		
        fetch("http://127.0.0.1:8000/Name/stat_hypothesis_api/", requestOptionsStatApi)
			.then(response => response.json())
			.then(r => {
				console.log(r)
				return r
			})
            .then(res => {
				
				let new_plot = {
					UUID: res.UUID,
					GigachainData: res.gigachainData,
					PlotType: res.plotType,
					PlotData: {
						X: res.plotData.X,
						Y: res.plotData.Y,
						Z: res.plotData.Z,
						Styles: {
							Color: res.plotData.style.Color,
							PlotSize: res.plotData.style.plotSize
						}
					},
					Error: "",
				}
				set_bot_message(new_plot)
				return res
            })
			.then(res => {
				let bot_answer = {
					user: false, // если сообщение пользователя - true, ответ сервера - false
					UUID: res.UUID,
					date: moment().format("hh:mm, DD.MM.YY"),
					Message: { 
						text: res.gigachainData,
						PlotType: res.plotType,
						PlotData: {
							X: res.plotData.X,
							Y: res.plotData.Y,
							Z: res.plotData.Z,
							Styles: {
								Color: res.plotData.style.Color,
								PlotSize: res.plotData.style.plotSize
							}
						},
					Error: "",
					}
				}

				history?.result.push(bot_answer)
				set_input_message("")
				setSpinner(false)
			})
    }

	useEffect(() => {
		if (getCookie("uuid") == undefined){
			fetch("http://127.0.0.1:8000/Name/add_user/")
            .then(response => response.json())
			.then(response => {
				setCookie("uuid", response.UUID)
				return response
			})
		}
    }, [])

	useEffect(() => {

		const init_user_header = {
			"Content-Type": "application/json",
			UUID: getCookie("uuid") as string,
		}
		const requestHeaders: HeadersInit = new Headers();
		requestHeaders.set('Content-Type', 'application/json');
		requestHeaders.append("UUID", getCookie("uuid") as string);
		
		const requestOptionsMessageApi = {
			method: 'GET',
			headers: requestHeaders,
		};


        fetch("http://127.0.0.1:8000/Name/message_api?UUID=" + getCookie("uuid") as string)
            .then(response => response.json())

			.then(r => {
				return r
			})
			.then(response => {
				let messages_array: any[] = response.result
				let new_message_list: ChatHistory = {result: []}
				messages_array.forEach(element => {
					let result_i = {
						user: element.user, // если сообщение пользователя - true, ответ сервера - false
						UUID: element.UUID,
						date: element.date,
						Message: { 
							text: element.Message.text,
							PlotType: element.Message.PlotType, // пустое поле, если user=true
							PlotData: {
								X: element.Message.PlotData.X, // пустое поле, если user=true
								Y: element.Message.PlotData.Y, // пустое поле, если user=true
								Z: element.Message.PlotData.Z, // пустое поле, если user=true
								Styles: {
									Color: element.Message.PlotData.Styles.Color, // пустое поле, если user=true
									PlotSize: element.Message.PlotData.Styles.PlotSize, // пустое поле, если user=true
								},
							},
						Error: element.Error,
						}
					}
					new_message_list.result.push(result_i)
				});
				set_history(new_message_list)
			})
    }, [])
	

	return (
		<div className='main-cell'>
			<div className='description'>
				<div className='title'>
					DEEPHACK.AGENTS
				</div>
				<div className='faq-link'>
					<a href='https://github.com/Quantum-calculators/DEEPHACK.AGENTS/blob/main/README.md'>FAQ</a>
				</div>
				
			</div>

			<div className='chat'>
				<div className='area-outside'>
					<div className='area-inside'>
						<div className='messeges-area'>
							<MessageShow story={history}/>
							{spinner ? (
								<SyncLoader 
									color='#4667DD'
									cssOverride={{padding: "25px"}}
								/>
							) : (<></>)}
							
						</div>
						
						<div className='input-area'>
							<input id='InputMessageElement' className='input-message' value={input_message} onChange={(e) => set_input_message(e.target.value)} type="text"/>
							<button id='SendMessageButton' className='send-message' onClick={post}>
								&rarr;
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default App;






