class Stack(list):
    def isEmpty(self):
        return len(self) == 0
    
    def push(self, elem):
        self.append(elem)

    def peek(self):
        return self[-1]

    def size(self):
        return len(self)


def check_sequence_correct(sequence):
    match_dict = {
        '(': ')',
        '[': ']',
        '{': '}'
    }

    my_stack = Stack()

    for elem in sequence:
        if my_stack.isEmpty():
            my_stack.push(elem)
        elif match_dict.get(my_stack.peek()) == elem:
            my_stack.pop()
        else:
            my_stack.push(elem)

    if my_stack.size():
        return False
    else:
        return True


if __name__ == '__main__':
    sequences = [
        '(((([{}]))))',
        '[([])((([[[]]])))]{()}',
        '{{[()]}}',
        '}{}',
        '{{[(])]}}',
        '[[{())}]'
    ]

    for sequence in sequences:
        if check_sequence_correct(sequence):
            print(f'sequence {sequence} correct!')
        else:
            print(f'sequence {sequence} incorrect!')





    