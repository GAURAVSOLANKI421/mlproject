import sys
from logger import logging

def error_message_detail(error , error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name= exc_tb.tb_frame.f_code.co_filename
    error_message = f"error occured in python script name {file_name},line number {exc_tb.tb_lineno} , error message {str(error)}"
    return error_message


class custom_exception(Exception):
    def __init__(self, error_message ,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error=error_message,error_detail=error_detail)

    def __str__(self) -> str:
        return self.error_message
    

if __name__ == "__main__":
    try:
        a=10/0
    except Exception as e:
        logging.info('logging has started')
        raise custom_exception(e,sys)
