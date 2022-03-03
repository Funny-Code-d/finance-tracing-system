from collections import namedtuple
import user_test
import purchase_test
import debtbook_test
import invest_account_test




StatusCode = namedtuple("StatusCode", ['name', 'code'])


class UnitTest():
    def __init__(self):
        self.tests = [
            user_test.Test(),
            purchase_test.Test(),
            debtbook_test.Test(),
            invest_account_test.Test(),
        ]
        
        
    def run():
        results = list()
        
        for unit in self.tests:
            # запуск юнит теста
            run_test = unit.run()
            
            # сохранение результатов
            if isinstance(run_test, list):
                # в классе было много тестов
                for result_test in run_test:
                    results.append(result_test)
                    
            elif isinstance(run_test, StatusCode):
                # в классе был один тест
                results.append(run_test)
        
        
        return results
            
    
    def display_result():
        r = self.Run()
        
        for unit in r:
            if unit.code == 0:
                print(f"Unit test {unit.name} is succsess")
            else:
                print("Unit test {unit.name} is failed")
                
        
if __name__ == "__main__":
    obj = UnitTest()
    obj.display_result()