import telebot
import cx_Oracle

host = 'x'
servico = 'x'
usuario = 'x'
senha = 'x'

# Encontra o arquivo que aponta para o banco de dados
cx_Oracle.init_oracle_client(lib_dir="./instantclient_21_10")

# Faz a conexão ao banco de dados
conecta_banco = cx_Oracle.connect(usuario, senha, f'{host}/{servico}')

# Cria um cursor no banco para que seja possível fazer consultas e alterações no banco de dados
cursor = conecta_banco.cursor()

# Este token é específico do bot criado
TOKEN = 'X'

# Crie uma instância do bot
bot = telebot.TeleBot(TOKEN)

# Função para executar o UPDATE e DELETE no banco de dados
def executar_update(numero):
    sql_update = f"""UPDATE PCEMPR 
                    SET USUARIOLOGADO = 'N',
                    NUMCONEXOESATUAL = 0,
                    DTINICIO = NULL,
                    TIPOATENDE = NULL
                    WHERE MATRICULA = {numero}"""
    sql_delete = f"DELETE FROM PCMENUSESSAO WHERE MATRICULA = {numero}"
    #sql_update = f"UPDATE sua_tabela SET coluna_numero = {numero} WHERE alguma_condicao = alguma_coisa"
    cursor.execute(sql_update)
    cursor.execute(sql_delete)
    cursor.execute("COMMIT")  # É importante fazer o commit após executar o update

# Função para executar o SELECT no banco de dados
def executar_select(texto):
    sql_select = f"SELECT matricula, nome FROM pcempr WHERE nome like '%{texto}%'"
    cursor.execute(sql_select)
    result = cursor.fetchall()
    return result

# Manipulador para mensagens recebidas
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if message.text.isdigit():
        numero = int(message.text)
        executar_update(numero)
        bot.send_message(chat_id, f"UPDATE realizado para o número: {numero}")
    else:
        texto = message.text
        resultado = executar_select(texto)
        if resultado:
            bot.send_message(chat_id, f"Resultado encontrado: {resultado}")
        else:
            bot.send_message(chat_id, "Nenhum resultado encontrado para o texto.")

# Inicia o bot
bot.polling()