

def func(l1, l2):
    ll = None
    while True:
        if l1 and l2:
            if l1.val > l2.val:
                val = l2.val
                l2 = l2.next
            else:
                val = l1.val
                l1 = l1.next
        elif l1:
            val = l1.val
            l1 = l1.next
        elif l2:
            val = l2.val
            l2 = l2.next
        else:
            return ll
        if ll:
            ll.next = ListNode(val)
        else:
            ll = ListNode(val)
        ll = ll.next

if __name__ == '__main__':

    func(l1, l2)
