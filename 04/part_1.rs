// 

fn cleck_rules(password: i32) -> bool {
    let mut i = 0
    hasAdjacent = False
    isMinToMax = False
    while i < 5:
        if str_password[i] == str_password[i + 1]:
            hasAdjacent = True
        if int(str_password[i]) <= int(str_password[i + 1]):
            isMinToMax = True
        else:
            isMinToMax = False


    if hasAdjacent and isMinToMax:
        return True
    else:
        return False
}

fn main() {
    let input_start = 273025
    let input_end = 767253
}
