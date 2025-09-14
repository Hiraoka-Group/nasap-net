from nasap_net import Assembly, Component, is_isomorphic

MX2 = Assembly(# (1)!
    {'M1': 'M', 'X1': 'X', 'X2': 'X'},
    [('M1.a', 'X1.a'), ('M1.b', 'X2.a')])

ANOTHER_MX2 = Assembly(# (2)!
    {'M100': 'M', 'X100': 'X', 'X200': 'X'},
    [('M100.a', 'X100.a'), ('M100.b', 'X200.a')])

COMPONENT_KINDS = {# (3)!
    'M': Component(['a', 'b']),
    'X': Component(['a']),
}

result = is_isomorphic(MX2, ANOTHER_MX2, COMPONENT_KINDS)# (4)!

print(f'Isomorphism check: {result}')# (5)!
