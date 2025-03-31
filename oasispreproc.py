import os
import re
import shutil
import nibabel as nib


def moveRename(source, dest):
    """
    Moves all .hdr and .img images from source location to a single directory
    """
    rawDirPat = r"(?:[\W\S]+?)OAS2_([0-9]{4})_MR([0-9]{1})/RAW"
    for root, dir, files in os.walk(source):
        r_match = re.findall(rawDirPat, root)
        if len(r_match) > 0:
            subID = r_match[0][0]
            session = r_match[0][1]
            new_name = f"{subID}_{session}"
            for f in files:
                fname, fext = os.path.splitext(f)
                if fext == ".img" or fext == ".hdr":
                    f_match = re.findall(r"mpr-([0-9]{1}).nifti", fname)
                    if len(f_match) > 0:
                        f_num = f_match[0]
                        old_name = os.path.join(root, f)
                        new_name = os.path.join(
                            dest, f"OAS2_{subID}_MR{f_num}_V{session}.nifti{fext}"
                        )
                        print(f"Copying {new_name}")
                        shutil.copy2(old_name, new_name)


def convertToNii(source):
    """
    Convert images from .img to .nii format and get rid of .img and .hdr files.
    """
    for root, dir, files in os.walk(source):
        for f in files:
            fbase, fext = os.path.splitext(f)
            if fext == ".img":
                print(f"Converting {f}")
                fname = os.path.join(root, f)
                img = nib.load(fname)
                nib.save(img, fname.replace(".img", ".nii"))
                os.remove(os.path.join(root, fbase + ".hdr"))
                os.remove(os.path.join(root, fbase + ".img"))


def removeVisits3to5(source):
    """
    Removes all images taken at visits 3-5
    """
    for root, dir, files in os.walk(source):
        for f in files:
            m = re.match(r"OAS2_[0-9]{4}_MR[0-9]{1}_V([0-9]{1})", f)
            session_num = int(m.groups()[0])
            if session_num >= 3:
                print(f"Removing {f}")
                os.remove(os.path.join(root, f))


if __name__ == "__main__":
    # moveRename("datasets/OAS2", "datasets/OAS2_nii")
    # convertToNii("datasets/OAS2_nii")
    # removeVisits3to5("datasets/OAS2_nii")
