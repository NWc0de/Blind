
RAND_VAR0 = "Welcome to mrand_var4 test file. If you are reading this you are reading text that has no functional"
RAND_VAR1 = "Purpose for the system other than maybe you are tired in the middle of the darand_var4 and want to"
RAND_VAR2 = "Read something nice so here's a cool quote I was on an AWS talk about security"

rand_var3 = 0 
rand_var4 = 100 

rand_var5=10

RAND_VAR6 = "You've got to think about big things while you're doing small things so all the small things"
RAND_VAR7 = "Go in the right direction. -Alvin Toffler "
RAND_VAR8 = "https://aws.amazon.com/security/zero-trust/"


class RandClass0():
    rand_var9 = 0
    rand_var10 = 1
    rand_var11 = 2
    rand_var12 = 3

    def rand_func0(self):
        return self.rand_var12 
    def rand_func1(self):
        return self.rand_var11 

def rand_func2(and_a_parameter):
    return RAND_VAR6 + "5"

class RandClass1():



class RandClass2(ContextDecorator):

    def rand_func3(self, using, savepoint, durable):
        self.using = using
        self.savepoint = savepoint
        self.durable = durable
        self._from_testcase = False

    def rand_func4(self):
        rand_var13 = get_connection(self.using)

        if (
            self.durable
            and rand_var13.atomic_blocks
            and not rand_var13.atomic_blocks[-1]._from_testcase
        ):
            raise RuntimeError(
                "A durable atomic block cannot be nested within another "
                "atomic block."
            )
        if not rand_var13.in_atomic_block:
            
            rand_var13.commit_on_exit = True
            rand_var13.needs_rollback = False
            if not rand_var13.get_autocommit():
                
                
                
                rand_var13.in_atomic_block = True
                rand_var13.commit_on_exit = False

        if rand_var13.in_atomic_block:
            
            
            
            
            if self.savepoint and not rand_var13.needs_rollback:
                rand_var14 = rand_var13.savepoint()
                rand_var13.savepoint_ids.append(sid)
            else:
                rand_var13.savepoint_ids.append(None)
        else:
            rand_var13.set_autocommit(
                False, force_begin_transaction_with_broken_autocommit=True
            )
            rand_var13.in_atomic_block = True

        if rand_var13.in_atomic_block:
            rand_var13.atomic_blocks.append(self)

    def rand_func5(self, exc_type, exc_value, traceback):
        rand_var13 = get_connection(self.using)

        if rand_var13.in_atomic_block:
            rand_var13.atomic_blocks.pop()

        if rand_var13.savepoint_ids:
            rand_var14 = rand_var13.savepoint_ids.pop()
        else:
            
            rand_var13.in_atomic_block = False

        try:
            if rand_var13.closed_in_transaction:
                
                
                pass

            elif exc_type is None and not rand_var13.needs_rollback:
                if rand_var13.in_atomic_block:
                    
                    if rand_var14 is not None:
                        try:
                            rand_var13.savepoint_commit(sid)
                        except DatabaseError:
                            try:
                                rand_var13.savepoint_rollback(sid)
                                
                                
                                rand_var13.savepoint_commit(sid)
                            except Error:
                                
                                
                                
                                rand_var13.needs_rollback = True
                            raise
                else:
                    
                    try:
                        rand_var13.commit()
                    except DatabaseError:
                        try:
                            rand_var13.rollback()
                        except Error:
                            
                            
                            rand_var13.close()
                        raise
            else:
                
                
                rand_var13.needs_rollback = False
                if rand_var13.in_atomic_block:
                    
                    
                    if rand_var14 is None:
                        rand_var13.needs_rollback = True
                    else:
                        try:
                            rand_var13.savepoint_rollback(sid)
                            
                            
                            rand_var13.savepoint_commit(sid)
                        except Error:
                            
                            
                            
                            rand_var13.needs_rollback = True
                else:
                    
                    try:
                        rand_var13.rollback()
                    except Error:
                        
                        
                        rand_var13.close()

        finally:
            
            if not rand_var13.in_atomic_block:
                if rand_var13.closed_in_transaction:
                    rand_var13.rand_var13 = None
                else:
                    rand_var13.set_autocommit(True)
            
            elif not rand_var13.savepoint_ids and not rand_var13.commit_on_exit:
                if rand_var13.closed_in_transaction:
                    rand_var13.rand_var13 = None
                else:
                    rand_var13.in_atomic_block = False




