import os

IDENT = 4

registers_64 : set = set(['rax','rcx','rdx','rbx','rsp','rbp','rsi','rdi','r8','r9','r10','r11','r12','r13','r14','r15'])
registers_32 : set = set(['eax','ecx','edx','ebx','esp','ebp','esi','edi','r8d','r9d','r10d','r11d','r12d','r13d','r14d','r15d'])
registers_16 : set = set(['ax','cx','dx','bx','sp','bp','si','di','r8w','r9w','r10w','r11w','r12w','r13w','r14w','r15w'])
registers_8 : set = set(['ah','al','ch','cl','dh','dl','bh','bl','spl','bpl','sil','dil','r8b','r9b','r10b','r11b','r12b','r13b','r14b','r15b'])
numbers : set = set(['0','1','2','3','4','5','6','7','8','9'])
operators : set = set(['+','-',','])

def add_newline(text:str):
    if len(text)==0 or text[-1] != '\n':
        return text+'\n'
    return text

def add_operator_space(text:str,op:str):
    if op not in text or '\'' in text or '`' in text or '\"' in text:
        return text.strip()
    splitted_text : str = text.split(sep=op)
    new_text : str = ""
    for i,current_text in enumerate(splitted_text):
        if i != len(splitted_text)-1:
            new_text += current_text.strip() + ' ' + op + ' '
        else:
            new_text += current_text
    return new_text

def take_asm_files(file_names : list[str]):
    new_files : list[str] = []
    
    for file in file_names:
        if '.asm' in file:
            new_files.append(file)
    return new_files

def count_first_spaces(text:list[str],sep:str):
    
    count : int = 0
    for word in text:
        if word != sep:
            break
        count += 1
    return count

def main_loop():
    dir : str = os.curdir
    files = os.listdir(dir)
    for file_name in take_asm_files(files):
        with open(file_name,"r") as f:
            text : list[str] = f.readlines()
        updated_text : list[str] = []
        with open(file_name, "w") as f:
            current_ident : int = 0
            for line in text:
                line = line.replace('\t',IDENT*' ')
                new_line : str = ''
                split_semicolon : list[str] = line.split(sep=';')
                if ';' in line:
                    if len(split_semicolon) == 1:
                        updated_text.append(current_ident*'\t'+ '; ' + add_newline(split_semicolon[0]).strip())
                        continue
                    elif len(split_semicolon) == 2:
                        updated_text.append(current_ident*'\t'+'; ' + add_newline(split_semicolon[1]).strip())
                current_line : str = split_semicolon[0]
                current_instructions = current_line.split(sep=' ')
                current_ident_space : int = count_first_spaces(current_instructions,sep='')//IDENT
                current_ident_tab : int = count_first_spaces(current_instructions,sep='\t')
                current_ident = max(current_ident_space,current_ident_tab)
                for item in current_instructions.copy():
                    if item == '':
                        current_instructions.remove('')
                new_line += current_instructions[0].strip()
                
                for i in range(1,len(current_instructions)):
                    ins : str = current_instructions[i].strip()
                    if '' == ins:
                        continue
                    for op in operators:
                        ins = add_operator_space(ins,op)
                    new_line += ' ' + ins.strip()
                updated_text.append(current_ident*'\t'+(add_newline(new_line.strip('\t')).strip(' ')))
            f.writelines(updated_text)