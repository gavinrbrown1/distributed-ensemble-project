# delete me later

from neural_network import load_network, classify

net = load_network()

for num in ['2','3','4']:
    print(num)
    prediction = classify(net, '../images/image_'+num+'.jpeg', 0, 0)
    print(prediction)
    print()
