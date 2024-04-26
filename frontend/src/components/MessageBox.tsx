interface IMessageBoxProps{
	is_user: boolean;
	date: string;
	message: string;
	plot?: HTMLBaseElement;
}


export function MessageBox(props: IMessageBoxProps){
	let actor = "bot"
	if (props.is_user){
		actor = "user"
	}
	return (
		<div id={props.date + "row"} className='massage-row'>
			<div id={props.date + "box"} className={'message-box-container-' + actor}>
				<div id={props.date + "data"} className={'message-data-' + actor}>
					{props.date}
				</div>
				<div className={'message-data-' + actor}>
					{props.message}
				</div>
			</div>
		</div>
		
	)
}
