import PyV8

ct = PyV8.JSContext()
ct.enter()
func = ct.eval(
"""
    (function(){
        function hi(){
            return "Hi!";
        }
        return hi();
    })
"""
)

print(func()) # 输出"Hi!"
