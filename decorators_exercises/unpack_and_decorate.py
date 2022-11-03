def with_job_title(func):
    def wrapper(*arg,**kwargs):
        func(job_title='Software Engineer',*arg,**kwargs)
    return wrapper

list = ['IT Technician','Today', 'Never']
dictionary = {
    "Job Title":'job_title',
    "Start Date":'start_date',
    "Finish Date":'finish_date'    
    }

@with_job_title
def function_that_takes_3_args(job_title,start_date,finish_date):
    list=[job_title,start_date,finish_date]
    dictionary = { 
        "Job Title":job_title,
        "Start Date":start_date,
        "Finish Date":finish_date,   
        }
    print(list, dictionary)


function_that_takes_3_args(*list)



def fun(a,b,c,d):
    print(a,b,c,d)

my_list =[1,2,3,4]

fun(*my_list)
