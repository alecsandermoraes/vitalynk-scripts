from typing import Union, Optional, BinaryIO, TextIO 
import logging, os 

_default_logger = logging.getLogger(__name__)
_default_logger.addHandler(logging.NullHandler())

def create_file(file_path: str, content: Optional[Union[str, bytes]] = None, mode: str = 'w', encoding: Optional[str] = 'utf-8', overwrite: bool = False, create_parent_dirs: bool = True, logger: Optional[logging.Logger] = None) -> bool:
    log = logger if logger else _default_logger 
    
    if not file_path:
        log.error('Caminho do arquivo não pode ser vazio')
        raise ValueError('Caminho do arquivo inválido')
    
    if not isinstance(mode, str) or mode not in ('w', 'wb', 'a', 'ab'):
        log.error(f'Modo de arquivo inválido: {mode}')
        raise ValueError('Modo deve ser "w", "wb", "a" ou "ab"')
    
    if os.path.exists(file_path) and not overwrite:
        log.warning(f'Arquivo já existe: {file_path}')
        return False 
    
    if create_parent_dirs:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok = True)
        except OSError as e:
            log.error(f'Erro ao criar diretórios: {e}')
            return False
    
    is_binary = 'b' in mode 
    
    if content is not None:
        if is_binary and not isinstance(content, bytes):
            log.error('Conteúdo deve ser bytes para modo binário')
            raise ValueError('Tipo de conteúdo incompatível com modo binário')
        elif not is_binary and not isinstance(content, str):
            log.error('Conteúdo deve ser string para modo texto')
            raise ValueError('Tipo de conteúdo incompatível com modo texto')
        
    try:
        with open(file_path, mode = mode, encoding = encoding if not is_binary else None) as file:
            if content is not None:
                file.write(content)
        log.info(f'Arquivo criado com sucesso: {file_path}')
        return True 
    except OSError as error:
        log.error(f'Falha ao criar arquivo: {error}')
        raise 
    except Exception as error:
        log.error(f'Erro inesperado: {error}')
        raise 

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    
    create_file(
        file_path = '/tmp/exemplo.txt',
        content = 'Conteúdo de exemplo',
        overwrite = True
    )
    
    create_file(
        file_path = '/tmp/exemplo.bin',
        content = b'\x01\x02\x03',
        mode = 'wb'
    )