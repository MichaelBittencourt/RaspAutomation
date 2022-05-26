#!/bin/bash
#
# initVideoStream.sh
#
# Inicia stream de video pelo vlc
#
# Versão 1: Exibe menu de ajuda, versao  e recebe largura e altura com parametro -r 
#
# Michael Bittencourt, Fevereiro de 2018
#

MENSAGEM_USO="
Uso $0 [-h | -v ] ou source $(basename "$0")

  -h, --help		 Mostra esta tela de ajuda e sai
  -v, --version		 Mostra a versão e sai
  -r, --reolution	 Informa resolucao do video separa por espaco, largura e alturaMostra a versão e sai
  -p, --port         Informa a porta


EX
  $0 --help	           Assim exibe o menu de ajuda do $(basename "$0")
  $0 --version	           Assim exibe a versao do $(basename "$0")
  $0 --resolution 640 360   Assim ele executa o script informando a largura e altura do video
  $0 --port 8554   Abre a conexão na porta 8554"

largura=640
altura=480
port=8554

if test -n "$1" 
then
	while test -n "$1"
	do
		case "$1" in
			-h | --help)
				echo "$MENSAGEM_USO"
				exit 0
			;;
			-v | --version)
				echo -n $(basename "$0")
				# Extrai versão diretamente dos cabeçalhos do programa
				grep '^# Versão ' "$0" | tail -1 | cut -d : -f 1 | tr -d \#
				exit 0
			;;
		    -r | --resolution)
				shift
			    if test -n "$1"
				then
					largura=$1
					altura=$2
					shift	
				fi	
			;;
            -p | --port)
				shift
			    if test -n "$1"
				then
					port=$1
				fi	
			;;
			*)
				if test -n "$1"
				then
					echo Opção inválida: $1
					echo "Tente $0 --help"
					exit 1
				fi
			;;
		esac
		shift
	done
fi

#-l option allow wait for connection
#-n option don't show stream locally
set -xv
raspivid -t 0 -n -b 1000000 -w $largura -h $altura -fps 15 -o - | cvlc -vvv stream:///dev/stdin --no-autoscale --sout "#rtp{sdp=rtsp://:$port/}" :demux=h264
