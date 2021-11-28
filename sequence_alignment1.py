def alignment(a,b):
    m = len(a)
    n = len(b)
    dp = [[0 for col in range(m+1)] for row in range(n+1)]
    mismath_pen = [[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]
    gap_pen = 30
    d = {"A":0, "C":1, "G":2, "T":3}
    temp_a = ""
    temp_b = ""
    for i in range(m+1):
        dp[0][i] = i*gap_pen
    for j in range(n+1):
        dp[j][0] = j*gap_pen
    for y in range(1,n+1):
        for x in range(1,m+1):
            mismatch = mismath_pen[d[a[x-1]]][d[b[y-1]]] + dp[y-1][x-1]
            gap_a = gap_pen + dp[y-1][x]
            gap_b = gap_pen + dp[y][x-1]
            dp[y][x] = min(mismatch, gap_a, gap_b)

    #retrieve actual alignment
    max_len = n + m # maximum possible length
     
    i = m
    j = n
     
    a_pos = max_len+1
    b_pos = max_len+1
 
    #Final answers for the respective strings
    a_ret = [0] * (max_len+1)
    b_ret = [0] * (max_len+1)
     
    while (i != 0 and j != 0):
        if a[i - 1] == b[j - 1]:
            a_pos -=1
            b_pos -=1
            a_ret[a_pos] = ord(a[i - 1])
            b_ret[b_pos] = ord(b[j - 1])
            i-=1
            j-=1
        elif (dp[j - 1][i - 1] + mismath_pen[d[a[i-1]]][d[b[j-1]]]) == dp[j][i]:
            a_pos -=1
            b_pos -=1
            a_ret[a_pos] = ord(a[i - 1])
            b_ret[b_pos] = ord(b[j - 1])
            i-=1
            j-=1
        elif (dp[j - 1][i] + gap_pen) == dp[j][i]:
            a_pos -=1
            b_pos -=1
            a_ret[a_pos] = ord('_')
            b_ret[b_pos] = ord(b[j - 1])
            j-=1
        elif (dp[j][i - 1] + gap_pen) == dp[j][i]:
            a_pos -=1
            b_pos -=1
            a_ret[a_pos] = ord(a[i - 1])
            b_ret[b_pos] = ord('_')
            i-=1
        
    while a_pos > 0:
        a_pos -=1
        if i > 0:
            i-=1
            a_ret[a_pos] = ord(a[i])
        else:
            a_ret[a_pos] = ord('_')
    while b_pos > 0:
        b_pos -=1
        if j > 0:
            j-=1
            b_ret[b_pos] = ord(b[j])
        else:
            b_ret[b_pos] = ord('_')
 
    # Find first index the alignment will start from
    start_index = 1;
    for i in range(max_len,0,-1):
        if chr(a_ret[i]) == '_' and chr(b_ret[i]) == '_':
            start_index = i + 1
            break
        
    #final string to be returned
    final_a = ""
    final_b = ""
    for i in range(start_index,max_len+1):
        final_a += chr(a_ret[i])
    final_a += "\n"
    for i in range(start_index,max_len+1):
        final_b += chr(b_ret[i])
    print(final_a)
    print(final_b)

    return dp[n][m]

