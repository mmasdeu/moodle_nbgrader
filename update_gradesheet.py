import nbgrader, csv, codecs, sys, os, shutil
from nbgrader.apps import NbGraderAPI
import zipfile
verbose = False
from i18n import *

def zip(out, root):
    shutil.make_archive(out, 'zip', root)

def moodle_gradesheet(assignment, with_feedback=True):

    api = NbGraderAPI()
    gradebook = api.gradebook
    csvfile = os.path.join("imports", assignment+".csv")
    with open(csvfile, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        fname =  os.path.join("exports", assignment+".csv")

        if with_feedback:
            archive = zipfile.ZipFile(os.path.join("exports", "feedback_"+assignment+".zip"), 'w', zipfile.ZIP_DEFLATED)
        with open(fname, 'w', encoding='utf-8', newline='') as out:
            writer = csv.DictWriter(out, reader.fieldnames)
            writer.writeheader()
            for line in reader:
                email, ident, fullname, status, grade, max_grade = line[email_str], line[ident_str], line[fullname_str], line[status_str], line[grade_str], line[max_grade_str]
                unique_id = email[0:7]
                try:
                    submission = gradebook.find_submission(assignment, unique_id)
                except:
                    if submitted_str in status:
                        print("WARNING: No submission for {id} in assignment {assign}".format(id=unique_id ,assign=assignment))
                    else:
                        if verbose:
                            print("\tNo submission for {id} in assignment {assign}, as expected".format(id=unique_id, assign=assignment))
                else:
                    if verbose:
                        print("\tProcessing submission for {id} in assignment {assign}".format(id=unique_id, assign=assignment))


                    fbk_path = os.path.join("feedback", unique_id, assignment)
                    try:
                        files = [os.path.join(fbk_path, f) for f in os.listdir(fbk_path) if f.endswith('.html')]
                        assign_id = ident[-6:]

                        # create the path to the feedback file
                        fbk_full_path = "{fullname}_{assign_id}_assignsubmission_file_".format(fullname=fullname, assign_id=assign_id)
                        for f in files:
                            archive.write(f, arcname=os.path.join(fbk_full_path, os.path.basename(f)))
                    except FileNotFoundError:
                        print("HTML feedback file for {fullname} {id} {assign} is missing".format(id=unique_id,
                        fullname=fullname, assign=assignment))
                        # no feedback to generate
                    line[grade_str] = submission.score

                    # warn about dubious scores
                    grade_int = 0 if line[grade_str] == '' else int(line[grade_str])
                    if grade_int <=0 or grade_int > submission.max_score:
                        print("Warning: {matric} {name} has a score of {grade}".format(matric=unique_id, name=fullname, grade=grade_int))

                    # correct the maximum grade
                    line[max_grade_str] = str(submission.max_score)
                    writer.writerow(line)

            print("Wrote to {0}".format(fname))

            # tidy up the feedback file
            if with_feedback:
                archive.close()
                    
            
if __name__=="__main__":
    if len(sys.argv)!=2:
            print("""
            Usage:
            
                update_gradesheet.py <assign> 
                
            Updates a CSV file gradesheet (which must have be downloaded from
            Moodle with "offline gradesheets" enabled in the assignment settings) with
            the results from grading the assignment <assign>.
            
            The input will be imports/<assign>.csv
            The output will be in exports/<assign>.csv
            
            Feedback will be zipped up into the file exports/<assign>_feedback.zip and this
            can be uploaded to Moodle if "Feedback files" is enabled. This uploads all student
            feedback in one go.
            
            """)
            exit(-1)
    
    assignment= sys.argv[1]
    print("Updating gradesheet for {0}...".format(assignment))
    moodle_gradesheet(assignment)
    
