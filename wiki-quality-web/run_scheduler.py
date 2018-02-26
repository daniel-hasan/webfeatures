'''
Created on 23 de fev de 2018

@author: Daniel Hasan Dalip
'''
import argparse




if __name__ == '__main__':
    from scheduler.performance_test.performance_test import create_database, \
    run_scheduler, write_performance_test
    

    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="Action: create a database (createdb) or run the scheduler (runscheduler) or save processment statistics (savestatistics)")
    parser.add_argument("datasets", help="Number of datasets to add/added",type=int)
    parser.add_argument("schedulers", help="Number of scheduler used. Just to save the parameter. This will not create schedulers.",type=int)
    
    args = parser.parse_args()
    if(args.action.lower()=="createdb"):
        create_database(args.schedulers, args.datasets)    
    elif(args.action.lower()=="runscheduler"):
        run_scheduler()
    elif(args.action.lower()=="savestatistics"):
        write_performance_test()
    else:
        print("Invalid action. The choices are: createdb, runscheduler and savestatistics")
