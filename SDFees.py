import requests
from web3 import Web3, contract, HTTPProvider
import time, json
import decimal
bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())


transaction ='0xfbcb306ad18685dbfa68b00e61df5102e01ed57d4640e14c7d1681bfa6d23a99'; 
count = 0
wei = 1000000000000000000 


# Pretty Json Data
print (json.dumps(json.loads(Web3.toJSON(web3.eth.get_transaction_receipt(transaction))),indent=4))
print (json.dumps(json.loads(Web3.toJSON(web3.eth.get_transaction(transaction))),indent=4))
transaction_Logs = json.loads(Web3.toJSON(web3.eth.get_transaction_receipt(transaction)))['logs']

# Json Data
transaction_Gas_Json = json.loads(Web3.toJSON(web3.eth.get_transaction_receipt(transaction)))['gasUsed']
transaction_Value_Json = json.loads(Web3.toJSON(web3.eth.get_transaction(transaction)))
# BSC fee
transaction_Gas = transaction_Gas_Json * 0.000000005
transaction_Value = transaction_Value_Json['value']/wei
# SD fee
entering_Farm_Fee = transaction_Value * .01
# PCS fee
swap_Fee = (transaction_Value - entering_Farm_Fee) * .0025
# Swap fee dec length (to prevent scientific notation)
swap_dec = decimal.Decimal(str(swap_Fee))
swap_dec_Len = abs(swap_dec.as_tuple().exponent)


# Math
total_Fee = round(transaction_Gas + swap_Fee + entering_Farm_Fee, 8)
total_Farm = (transaction_Value - entering_Farm_Fee) / 2
total_Fees_Percentage = total_Fee/transaction_Value * 100
single_farm_fee_String = str(swap_Fee/2)
single_farm_fee = swap_Fee/2

# Fee length
fee_dec = decimal.Decimal(str(total_Fee))
fee_dec_Len = abs(fee_dec.as_tuple().exponent)
print('kek', fee_dec_Len)

# Gas Fee Length
gas_fee_dec = decimal.Decimal(str(transaction_Gas))
gas_fee_dec_Len = abs(gas_fee_dec.as_tuple().exponent)
print('kek', gas_fee_dec_Len)

# SD Fee length
sd_fee_dec = decimal.Decimal(str(single_farm_fee))
sd_fee_dec_Len = abs(sd_fee_dec.as_tuple().exponent)
print('kek', sd_fee_dec_Len)

# Table
from prettytable import PrettyTable
x = PrettyTable()
x.title = f"Deposit Fees for {transaction_Value} BNB Stake"
x.field_names = [f'Total Fees: {total_Fee} BNB', "Value"]
x.add_row(['BSC Gas Fee', f'{transaction_Gas:.{gas_fee_dec_Len}f}' + ' BNB'])
x.add_row(['Entering Farm on SimpleDefi - 0.1%', str(entering_Farm_Fee) + ' BNB'])
x.add_row(['PanCakeSwap Fee for BNB -> Token A - 0.25%', f'{single_farm_fee:.{swap_dec_Len}f}' + ' BNB'])
x.add_row(['PanCakeSwap Fee for BNB -> Token B - 0.25%', f'{single_farm_fee:.{swap_dec_Len}f}' + ' BNB'])
x.add_row(['Total Fee', f'{total_Fee:.{swap_dec_Len}f}' + ' BNB'])


print(x)





